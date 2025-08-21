from django.db import models
from django.utils.translation import gettext as _
from authentication.models import Student

class Role(models.IntegerChoices):
    TEACHER = 0, _('Teacher')
    STAFF = 1, _('Staff')
    SUPERVISOR = 2, _('Supervisor')


class Teacher(models.Model):
    user = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True)
    role = models.IntegerField(choices=Role.choices, default=Role.STAFF)
    salary = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        if self.user:
            return self.user.username
        else:
            return super().__str__()
