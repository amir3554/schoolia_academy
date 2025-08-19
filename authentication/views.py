from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from .forms import StudentCreationForm, ChangeUserPasswordForm, StudentUpdateForm
from .models import Student
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class RegisterView(CreateView):
    form_class = StudentCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class ChangePasswordView(LoginRequiredMixin, CreateView):
    form_class  = ChangeUserPasswordForm
    success_url = reverse_lazy('DiariesList')
    template_name = ''

class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Student
    template_name = 'Profile.html'
    pk_url_kwarg = 'user_id'

    def test_func(self):
        return (self.request.user == self.get_object())


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'profile_edit.html'
    pk_url_kwarg = 'user_id'

    def test_func(self):
        return (self.request.user == self.get_object())

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('EditProfile', args=[self.object.id])