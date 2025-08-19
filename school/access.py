from django.utils.functional import cached_property
from operation.models import Transaction, TransactionStatus

class CourseAccess:
    def __init__(self, student, course):
        self.student = student
        self.course = course

    #@cached_property
    #def enrolled(self):
    #    return self.course.students.filter(id=self.student.pk).exists()

    @cached_property
    def __paid(self):
        return Transaction.objects.filter(
            course=self.course,
            student=self.student,
            status=TransactionStatus.COMPLETED
        ).exists()

    @cached_property
    def allowed(self):
        return self.__paid