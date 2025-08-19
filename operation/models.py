from django.db import models
from school.models import Course 
from authentication.models import Student

class PaymentMethod(models.IntegerChoices):
    STRIPE = 2, 'Stripe'

class TransactionStatus(models.IntegerChoices):
    PENDING = 0, 'Pending'
    COMPLETED = 1, 'Completed'
    CANCELED = 2, 'Canceled'


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=TransactionStatus.choices, default=TransactionStatus.PENDING)
    payment_method = models.IntegerField(choices=PaymentMethod.choices, null=True)
    transaction_id_webhook = models.CharField(max_length=100,unique=True,blank=True,null=True,help_text='Transaction number from payment gateway (webhook)')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def student_name(self):
        return self.student.first_name + ' ' + self.student.last_name                                            #type:ignore
    
    @property
    def student_email(self):
        return self.student.email                                                                                #type:ignore

    def __str__(self):
            return f"Payment:{self.pk} - amount:{self.amount} -  {self.status}"


    class Meta:
        unique_together = [['course', 'student']]
        indexes = [
                    models.Index(fields=['course', 'student', 'status']),
                    models.Index(fields=['course', 'status']),
                ]
