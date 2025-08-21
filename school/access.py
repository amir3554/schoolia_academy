from django.utils.functional import cached_property
from operation.models import Transaction, TransactionStatus
from teacher.models import Teacher, Role

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
    def __is_manager(self):
        return Teacher.objects.filter(user=self.student).exists()

    @cached_property
    def allowed(self):
        return self.__paid 
    

class SchoolManagerCheck:
    def __init__(self, user) -> None:
        self.user = user


    @cached_property
    def is_teacher(self):
        return Teacher.objects.filter(user=self.user, role=Role.TEACHER).exists()
    
    @cached_property
    def is_supervisor(self):
        return Teacher.objects.filter(user=self.user, role=Role.SUPERVISOR).exists()

