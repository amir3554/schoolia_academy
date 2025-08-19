from django.shortcuts import get_object_or_404
from .models import Course
from .access import CourseAccess

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
        
        try:
            request.course = Course.objects.only('id').get(pk=cid)
            request.course_access = CourseAccess(request.user, request.course).allowed

        except Course.DoesNotExist:
            request.course = None
            request.course_access = None

        return None
