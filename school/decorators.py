from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Course
from operation.models import Transaction, TransactionStatus


def has_course(course_kw='course_id', redirect_name='CheckOut', redirect_on_denied=True):

    def decorator(func): 

        @wraps(func)
        def _actual_wrapper(request, *args, **kwargs):

            cid = kwargs.get(course_kw)

            if cid is None:
                return HttpResponse("Error :No Course Id")
            
            course = get_object_or_404(Course.objects.only('id'), id=cid)
            student = request.user
            transaction = Transaction.objects.filter(
                course=course, 
                student=student,
                status = TransactionStatus.COMPLETED).first()
            if transaction is None:
                if redirect_on_denied:
                    return redirect(redirect_name, course.pk)
                else:
                    raise PermissionDenied
            else:
                kwargs['course'] = course
                return func(course, *args, **kwargs)

        return _actual_wrapper
        
    return decorator


def has_courses(redirect_name="BuyAll", redirect_on_denied=True):

    def decorator(func):

        @wraps(func)
        def _actual_wrapper(request, *args, **kwargs):
            transactions = Transaction.objects.filter(student=request.user, status=TransactionStatus.COMPLETED).all()
            courses = Course.objects.filter(transaction__in=transactions).all()

            is_teacher = getattr(request, 'is_teacher', None)
            is_supervisor = getattr(request, 'is_supervisor', None)
            teacher = getattr(request, 'teacher', None)

            if teacher or is_supervisor or is_teacher:
                if not transactions.exists() or not courses.exists():
                    if redirect_on_denied:
                        return redirect(redirect_name)
                    else:
                        return PermissionDenied
                    
                return func(request, courses, *args, **kwargs)

            if not transactions.exists() or not courses.exists():
                if redirect_on_denied:
                    return redirect(redirect_name)
                else:
                    return PermissionDenied

            return func(request, courses, *args, **kwargs)
        return _actual_wrapper
    return decorator



def require_course_access(redirect_name='CheckOut', redirect_on_denied=True):

    def deco(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            course = getattr(request, 'course', None)
            access = getattr(request, 'course_access', None)
            teacher = getattr(request, 'teacher', None)
            is_teacher = getattr(request, 'is_teacher', None)
            is_supervisor = getattr(request, 'is_supervisor', None)


            if (teacher) or (is_supervisor is True) or (is_teacher is True):
                return view_func(request, *args, **kwargs)

            if course is None:
                cid = kwargs.get('course_id') or kwargs.get('cid')

                if not cid:
                    raise Http404("Course id not found in URL.")
                
                from .models import Course
                course = Course.objects.only('id').filter(pk=cid).first()

                if not course:
                    raise Http404("Course not found.")
                
                request.course = course

            if not (access):
                if redirect_on_denied:
                    return redirect(redirect_name, request.course.pk)
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return deco



