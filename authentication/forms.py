from typing import Any
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from .models import Student

attrs = {'class' : 'form-control'}


class UserLoginForm(AuthenticationForm):
    
    def __init__(self,*args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs=attrs)
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs=attrs)
    )

class StudentCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs=attrs)
    )

    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs=attrs)
    )

    first_name = forms.CharField(
        label='first name',
        widget=forms.TextInput(attrs=attrs)
    )
    last_name = forms.CharField(
        label='last name',
        widget=forms.TextInput(attrs=attrs)
    )
    
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs=attrs)
    )

    password2 = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(attrs=attrs)
    )
    
    bio = forms.CharField(
        label='bio (Optional)',
        required=False,
        widget=forms.Textarea(attrs=attrs)
    )



    class Meta:
       model = Student
       fields = [
            'username', 'email', 'first_name', 'last_name', 
            'password1', 'password2', 'bio'
        ]
        
class ChangeUserPasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    current_password = forms.CharField(
        label='current password',
        widget=forms.PasswordInput(attrs=attrs)
    )

    new_password1 = forms.CharField(
        label='new password',
        widget=forms.PasswordInput(attrs=attrs)
    )

    new_password2 = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput(attrs=attrs)
    )

    class Meta:
        medel = Student
        #fields = []  # You usually don't need to specify fields here for PasswordChangeForm


class StudentUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    bio = forms.CharField(
    label='bio (Optional)',
    required=False,
    widget=forms.Textarea(attrs=attrs)
    )


    username = forms.CharField(
        label='user name',
        widget=forms.TextInput(attrs=attrs)
    )

    profile_image = forms.ImageField(
        label='profile image (Optional)',
        required=False,
        widget=forms.ClearableFileInput(attrs=attrs)
    )


    class Meta:
        model = Student
        fields = ['username', 'bio', 'profile_image']




