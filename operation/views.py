from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from schoolia import settings
from school.models import Course

import stripe
from stripe.error import SignatureVerificationError #type: ignore


from .models import Transaction , TransactionStatus, PaymentMethod

from .decorators import not_teacher

import math



def make_transaction(user_id, course_id, pm):
    course = get_object_or_404(
        Course,
        pk=course_id,
    )
    transaction, created  = Transaction.objects.get_or_create(
        defaults={
            'amount' : math.ceil(course.price),
            'payment_method' : pm,
        },
        course_id = course.pk,
        student_id = user_id
    )
    return transaction




def transaction_complete(transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    transaction.status = TransactionStatus.COMPLETED
    transaction.save()


@login_required
@not_teacher
def check_out(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id)
    
    if Transaction.objects.filter(
        student=request.user,
        course=course,
        status=TransactionStatus.COMPLETED).exists():
        
        return redirect("Course", course.pk)


    return render(
        request, 'check_out.html',
        {
            'course' : course
        }
    )


@login_required
def check_out_complete(request):
    return render(
        request, 'check_out_complete.html'
    )




def get_publishable_key(request):
    return JsonResponse(
        { 
            'publishable_key' : settings.STRIPE_PUBLISHABLE_KEY
        }
    )



@login_required
def stripe_transaction(request, course_id):
    try:
        transaction = make_transaction(request.user.pk, course_id, PaymentMethod.STRIPE)
    
        stripe.api_key = settings.STRIPE_SECRET_KEY

        intent = stripe.PaymentIntent.create(
            amount = int(transaction.amount * 100),
            currency=settings.CURRENCY,
            payment_method_types=['card'],
            metadata={
                'transaction' : transaction.pk
            }
        )
        return JsonResponse(
            {
                'client_secret': intent["client_secret"]
            }
        )

    except Exception as e:
        return JsonResponse(
            { 
                "message" : f"while making a transaction, please try again ...",
            },
            status = 400
        )


    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body # to get to the data of the request
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        stripe_event_webhook = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError:
        print('Invalid payload')
        return HttpResponse(status=400)
    
    except SignatureVerificationError:
        print('Invalid signature')
        return HttpResponse(status=400)
    
    try:
        if stripe_event_webhook.type == 'payment_intent.succeeded':
            payment_intent = stripe_event_webhook.data.object
            transaction_id = payment_intent.metadata.transaction #type:ignore
            transaction_complete(transaction_id)
        
    except:
        print("Exception in webhook:")
        return HttpResponse(status=422, message="Webhook payload is malformed or missing required fields")

    return HttpResponse(status=200)
