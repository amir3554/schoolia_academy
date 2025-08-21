from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from .models import Course
from .access import CourseAccess, SchoolManagerCheck
from teacher.models import Teacher, Role
from django.http import HttpResponse

class CourseAccessMiddleware:
    """
    يلتقط course_id/pk من ال-url kwargs ويثبت course + course_access على الطلب.
     يعمل فقط على مسارات الكورسات لتجنّب أي حمل زائد.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            return self.get_response(request)


    def process_view(self, request, view_func, view_args, view_kwargs):
        cid = (
            view_kwargs.get('course_id')
            or view_kwargs.get('cid')
        )
        if not cid:
            return None
        
        if not request.user.is_authenticated:
            return None
        
        try:
            request.course = Course.objects.only('id').get(pk=cid)
            request.course_access = CourseAccess(request.user, request.course).allowed

        except Course.DoesNotExist:
            request.course = None
            request.course_access = None

        return None


class ManagerAccessMiddleware:
     

    def __init__(self, get_response):
       self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):

        if not request.user.is_authenticated:
            return None

        try:
            request.teacher = Teacher.objects.get(user_id=request.user)
            request.is_teacher = SchoolManagerCheck(request.user).is_teacher
            request.is_supervisor = SchoolManagerCheck(request.user).is_supervisor
        except:
            request.teacher = None
            request.is_teacher = None
            request.is_supervisor = None

        return None