from django import forms
from django.utils.translation import gettext as _
from school.models import Course, Unit, Lesson


attrs = {'class' : 'form-control'}

class CourseModelForm(forms.ModelForm):

    class Meta:
        
        model = Course

        fields = ['name', 'description', 'price', 'image']

        labels = {
            'name' : _("name"),
            'description' : _("description"),
            'price' : _('price'),
            'image' : _('image'),
        }

        widgets = {
            'name' : forms.TextInput(attrs=attrs),
            'description' : forms.Textarea(attrs=attrs),
            'price' : forms.NumberInput(attrs=attrs),
            'image' : forms.FileInput(attrs=attrs)
        }


class UnitModelForm(forms.ModelForm):

    class Meta:
        
        model = Unit

        fields = ['name', 'description', 'course']

        labels = {
            'name' : _("name"),
            'description' : _("description"),
            'course' : _('course'),
        }

        widgets = {
            'name' : forms.TextInput(attrs=attrs),
            'description' : forms.Textarea(attrs=attrs),
            'course' : forms.Select(attrs=attrs),
        }


class LessonModelForm(forms.ModelForm):

    class Meta:
        
        model = Lesson

        fields = ['title', 'content', 'image', 'video', 'youtube_id', 'unit']

        labels = {
            'title' : _("title"),
            'content' : _("content"),
            'image' : _('image'),
            'video' : _('video'),
            'youtube_id' : _('youtube_id'),
            'unit' : _('unit'),
        }

        widgets = {
            'title' : forms.TextInput(attrs=attrs),
            'content' : forms.Textarea(attrs=attrs),
            'image' : forms.FileInput(attrs=attrs),
            'video' : forms.FileInput(attrs=attrs),
            'youtube_id' : forms.TextInput(attrs=attrs),
            'unit' : forms.Select(attrs=attrs),

        }