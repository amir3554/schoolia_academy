from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods 
from django.shortcuts import get_object_or_404
from school.models import Course, Unit, Lesson
from django.http import JsonResponse
from .models import Teacher, Role
from teacher.forms import CourseModelForm, UnitModelForm, LessonModelForm
import uuid
import random
from utils.s3 import upload_fileobj_to_s3, public_url


class CoursesManageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = "operations/main_manage.html"


    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor or is_teacher

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()
        

class UnitsManageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Unit
    template_name = "operations/manage_units.html"


    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor or is_teacher


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        if course_id is not None:
            course = get_object_or_404(Course.objects.only('id'), id=course_id)
            context['course'] = course
        return context


    def get_queryset(self) -> QuerySet[Any]:
        qs = (
            super()
            .get_queryset()
            .select_related("course")   # جلب FK بكفاءة
        )
        course_id = self.kwargs.get("course_id")
        if course_id is not None:
            qs = qs.filter(course_id=course_id)  # <-- احفظ الناتج
        return qs



class LessonsManageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Lesson
    template_name = "operations/manage_lessons.html"


    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor or is_teacher


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        if course_id is not None:
            course = get_object_or_404(Course.objects.only('id'), id=course_id)
            context['course'] = course
        return context


    def get_queryset(self) -> QuerySet[Any]:
        qs = (
            super()
            .get_queryset()
            .select_related("unit")   # جلب FK بكفاءة
        )
        unit_id = self.kwargs.get("unit_id")
        if unit_id is not None:
            qs = qs.filter(unit_id=unit_id)  # <-- احفظ الناتج
        return qs



class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'operations/create_course.html'

    
    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor
    
    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     self.object = form.save()
    #     return super().form_valid(form)


    def form_valid(self, form):

            self.object = form.save(commit=False)

            f = self.request.FILES.get("image")
            if f:
                try:
                    f.open()
                except Exception:
                    pass
                try:
                    f.seek(0)
                except Exception:
                    pass

                key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{f.name}"
                upload_fileobj_to_s3(f, key, content_type=f.content_type)
                self.object.image = public_url(key) 

                form.cleaned_data["image"] = None
                if "image" in form.files:
                    del form.files["image"]

            self.object.save()
            return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('UnitsManage', args=[self.object.pk])


class UnitCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Unit
    form_class = UnitModelForm
    template_name = 'operations/create_unit.html'

    
    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor


    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     self.object = form.save()
    #     return super().form_valid(form)

    def form_valid(self, form):

        self.object = form.save(commit=False)

        f = self.request.FILES.get("image")
        if f:
            try:
                f.open()
            except Exception:
                pass
            try:
                f.seek(0)
            except Exception:
                pass

            key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{f.name}"
            upload_fileobj_to_s3(f, key, content_type=f.content_type)
            self.object.image = public_url(key) 

            form.cleaned_data["image"] = None
            if "image" in form.files:
                del form.files["image"]

            self.object.save()
            return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('LessonsManage', args=[self.object.course.pk, self.object.pk])


class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonModelForm
    template_name = 'operations/create_lesson.html'

    
    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor


    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     self.object = form.save()
    #     return super().form_valid(form)

    def form_valid(self, form):

        self.object = form.save(commit=False)

        image = self.request.FILES.get("image")
        if image:
            try:
                image.open()
            except Exception:
                pass
            try:
                image.seek(0)
            except Exception:
                pass

            key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{image.name}"
            upload_fileobj_to_s3(image, key, content_type=image.content_type)
            self.object.image = public_url(key) 

            form.cleaned_data["image"] = None
            if "image" in form.files:
                del form.files["image"]

        video = self.request.FILES.get("video")
        if video:
            try:
                video.open()
            except Exception:
                pass
            try:
                video.seek(0)
            except Exception:
                pass

            key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{video.name}"
            upload_fileobj_to_s3(video, key, content_type=video.content_type)
            self.object.video = public_url(key) 

            form.cleaned_data["video"] = None
            if "video" in form.files:
                del form.files["video"]

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('Lesson', args=[self.object.unit.course.pk, self.object.pk])
    



class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'operations/create_course.html'

    
    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor or is_teacher


    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     self.object = form.save()
    #     return super().form_valid(form)

    def form_valid(self, form):

            self.object = form.save(commit=False)

            f = self.request.FILES.get("image")
            if f:
                try:
                    f.open()
                except Exception:
                    pass
                try:
                    f.seek(0)
                except Exception:
                    pass

                key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{f.name}"
                upload_fileobj_to_s3(f, key, content_type=f.content_type)
                self.object.image = public_url(key) 

                form.cleaned_data["image"] = None
                if "image" in form.files:
                    del form.files["image"]

            self.object.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('Course', args=[self.object.pk])


class UnitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Unit
    form_class = UnitModelForm
    template_name = 'operations/create_unit.html'

    
    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor or is_teacher


    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     self.object = form.save()
    #     return super().form_valid(form)

    def form_valid(self, form):

            self.object = form.save(commit=False)

            f = self.request.FILES.get("image")
            if f:
                try:
                    f.open()
                except Exception:
                    pass
                try:
                    f.seek(0)
                except Exception:
                    pass

                key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{f.name}"
                upload_fileobj_to_s3(f, key, content_type=f.content_type)
                self.object.image = public_url(key) 

                form.cleaned_data["image"] = None
                if "image" in form.files:
                    del form.files["image"]

            self.object.save()
            return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('Unit', args=[self.object.course.pk, self.object.pk])


class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonModelForm
    template_name = 'operations/create_lesson.html'

    
    def test_func(self):
        is_teacher = getattr(self.request, 'is_teacher', None)
        is_supervisor = getattr(self.request, 'is_supervisor', None)
        teacher = getattr(self.request, 'teacher', None)
        if teacher is None:
           return False
        if is_teacher is None:
           return False
        if is_supervisor is None:
           return False
        
        return is_supervisor or is_teacher


    # def form_valid(self, form: BaseModelForm) -> HttpResponse:
    #     self.object = form.save()
    #     return super().form_valid(form)

    def form_valid(self, form):

        self.object = form.save(commit=False)

        image = self.request.FILES.get("image")
        if image:
            try:
                image.open()
            except Exception:
                pass
            try:
                image.seek(0)
            except Exception:
                pass

            key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{image.name}"
            upload_fileobj_to_s3(image, key, content_type=image.content_type)
            self.object.image = public_url(key) 

            form.cleaned_data["image"] = None
            if "image" in form.files:
                del form.files["image"]

        video = self.request.FILES.get("video")
        if video:
            try:
                video.open()
            except Exception:
                pass
            try:
                video.seek(0)
            except Exception:
                pass

            key = f"media/courses/{random.randint(1, 1000)}-{random.randint(1, 1000)}-{video.name}"
            upload_fileobj_to_s3(video, key, content_type=video.content_type)
            self.object.video = public_url(key) 

            form.cleaned_data["video"] = None
            if "video" in form.files:
                del form.files["video"]

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('Lesson', args=[self.object.unit.course.pk, self.object.pk])
    




@login_required
@require_http_methods(['DELETE'])
def delete_course(request, pk):

    is_teacher = getattr(request, 'is_teacher', None)
    is_supervisor = getattr(request, 'is_supervisor', None)
    teacher = getattr(request, 'teacher', None)

    if teacher is None:
        return HttpResponseForbidden()
    if is_teacher is None:
        return HttpResponseForbidden()
    if is_supervisor is None:
        return HttpResponseForbidden()

    course = get_object_or_404(Course, id=pk)
    course.delete()
    return JsonResponse({'message': 'course deleted successfully.'}, status=204)


@login_required
@require_http_methods(['DELETE'])
def delete_unit(request, pk):
    is_teacher = getattr(request, 'is_teacher', None)
    is_supervisor = getattr(request, 'is_supervisor', None)
    teacher = getattr(request, 'teacher', None)

    if teacher is None:
        return HttpResponseForbidden()
    if is_teacher is None:
        return HttpResponseForbidden()
    if is_supervisor is None:
        return HttpResponseForbidden()
    unit = get_object_or_404(Unit, id=pk)
    unit.delete()
    return JsonResponse({'message': 'unit deleted successfully.'}, status=204)


@login_required
@require_http_methods(['DELETE'])
def delete_lesson(request, pk):
    is_teacher = getattr(request, 'is_teacher', None)
    is_supervisor = getattr(request, 'is_supervisor', None)
    teacher = getattr(request, 'teacher', None)

    if teacher is None:
        return HttpResponseForbidden()
    if is_teacher is None:
        return HttpResponseForbidden()
    if is_supervisor is None:
        return HttpResponseForbidden()
    lesson = get_object_or_404(Lesson, id=pk)
    lesson.delete()
    return JsonResponse({'message': 'lesson deleted successfully.'}, status=204)
