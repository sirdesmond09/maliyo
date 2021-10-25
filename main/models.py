from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.

def batch_date():
    return timezone.now().strftime('%B-%Y')
    
    
class Bank(models.Model):
    bank_name= models.CharField(max_length=200)
    paystack_code = models.CharField(max_length=200)
    
    def __str__(self):
        return self.bank_name
    
    

class StudentBankDetail(models.Model):
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    account_number = models.CharField(max_length=15)
    account_name = models.CharField(max_length=250)
    recipient_code = models.CharField(max_length=200, null=True, blank=True)
    month = models.CharField(default=batch_date, max_length=300)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.recipient_code
    
    @property
    def student_name(self):
        return self.student.name
    
    
    @property
    def bank_name(self):
        return self.bank.bank_name