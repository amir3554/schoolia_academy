from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from school.models import Course, Unit, Lesson
from .models import Teacher, Role
from teacher.forms import CourseModelForm, UnitModelForm, LessonModelForm


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'operations/create_course.html'

    
    def test_func(self):
        teacher = Teacher.objects.get(user=self.request.user)
        if teacher.DoesNotExist:
            return HttpResponseForbidden()
        return teacher.role == Role.SUPERVISOR


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('Course', args=[self.object.pk])


class UnitCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Unit
    form_class = UnitModelForm
    template_name = 'operations/create_unit.html'

    
    def test_func(self):
        teacher = Teacher.objects.get(user=self.request.user)
        if teacher.DoesNotExist:
            return HttpResponseForbidden()
        return teacher.role == Role.SUPERVISOR


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('Unit', args=[self.object.course_id, self.object.pk])


class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonModelForm
    template_name = 'operations/create_lesson.html'

    
    def test_func(self):
        teacher = Teacher.objects.get(user=self.request.user)
        if teacher.DoesNotExist:
            return HttpResponseForbidden()
        return teacher.role == Role.SUPERVISOR


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('Lesson', args=[self.object.course_id, self.object.pk])
    



class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseModelForm
    template_name = 'operations/update_course.html'

    
    def test_func(self):
        teacher = Teacher.objects.get(user=self.request.user)
        if teacher.DoesNotExist:
            return HttpResponseForbidden()
        return (teacher.role == Role.SUPERVISOR) or (teacher.role == Role.TEACHER)


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('Course', args=[self.object.pk])


class UnitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Unit
    form_class = UnitModelForm
    template_name = 'operations/update_unit.html'

    
    def test_func(self):
        teacher = Teacher.objects.get(user=self.request.user)
        if teacher.DoesNotExist:
            return HttpResponseForbidden()
        return (teacher.role == Role.SUPERVISOR) or (teacher.role == Role.TEACHER)


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('Unit', args=[self.object.course_id, self.object.pk])


class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonModelForm
    template_name = 'operations/update_lesson.html'

    
    def test_func(self):
        teacher = Teacher.objects.get(user=self.request.user)
        if teacher.DoesNotExist:
            return HttpResponseForbidden()
        return (teacher.role == Role.SUPERVISOR) or (teacher.role == Role.TEACHER)


    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        self.object = form.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('Lesson', args=[self.object.course_id, self.object.pk])