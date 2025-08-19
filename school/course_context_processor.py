def course_context(request):
    return {
        'course': getattr(request, 'course', None),
        'course_access': getattr(request, 'course_access', None),
    }