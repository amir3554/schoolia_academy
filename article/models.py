from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from authentication.models import Student


class Article(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    comments = GenericRelation(
        'school.Comment',
        content_type_field='receiver_content_type',
        object_id_field='receiver_object_id',
        related_query_name='article',
    )



    def __str__(self) -> str:
        return self.title
