from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from schoolia import settings
from authentication.models import Student



class Course(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
            return f"{self.name} : {self.price:.2f} {settings.CURRENCY}"

class Unit(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    video = models.FileField(null=True, blank=True)
    youtube_id = models.CharField(max_length=256, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comments = GenericRelation(
        'Comment',
        content_type_field='receiver_content_type',
        object_id_field='receiver_object_id',
        related_query_name='lesson',
    )


    def __str__(self) -> str:
        return self.title




class Notification(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title



class Comment(models.Model):
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    receiver_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    receiver_object_id = models.PositiveIntegerField()
    receiver = GenericForeignKey('receiver_content_type', 'receiver_object_id')
    children = GenericRelation(
        'Comment',
        content_type_field='receiver_content_type',
        object_id_field='receiver_object_id',
        related_query_name='parent',
    )


    def __str__(self) -> str:
        return self.content or f"comment#{self.pk}"
    
    