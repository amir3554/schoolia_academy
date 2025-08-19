from django import forms
from django.utils.translation import gettext as _
from article.models import Article


attrs = {'class' : 'form-control'}

class ArticleModelForm(forms.ModelForm):

    class Meta:
        
        model = Article

        fields = ['title', 'content', 'image']

        labels = {
            'title' : _("title"),
            'content' : _("content"),
            'image' : _('image'),
        }

        widgets = {
            'title' : forms.TextInput(attrs=attrs),
            'content' : forms.Textarea(attrs=attrs),
            'image' : forms.FileInput(attrs=attrs),
        }