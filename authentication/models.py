from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(AbstractUser):
    email = models.EmailField('email', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    bio = models.TextField(null=True, blank=True)
    courses = models.ManyToManyField('school.Course', related_name='students')

    def __str__(self):
        return self.first_name + ' ' + self.last_name





