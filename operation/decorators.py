from teacher.models import Teacher
from functools import wraps
from django.shortcuts import redirect


def not_teacher(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):

        if Teacher.objects.filter(user=request.user).exists():
            return redirect("CheckOutComplete")
        
        return func(request, *args, **kwargs)
    
    return wrapper

