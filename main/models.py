from django.db import models
from django.utils import timezone

# Create your models here.

def batch_date():
    return timezone.now().strftime('%B-%Y')
    
class Student(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    batch = models.CharField(default=batch_date, max_length=200)
    time_added = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    def delete(self):
        self.is_active=False
        self.save()
        
        return
    
    
    def __str__(self):
        return self.name
    

class OTP(models.Model):
    code = models.CharField(max_length=6)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='otps')
    expiry_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=2))
    
    
    def expired(self):
        return timezone.now() > self.expiry_date
    
    def __str__(self):
        return self.code
    
class Bank(models.Model):
    bank_name= models.CharField(max_length=200)
    paystack_code = models.CharField(max_length=200)
    
    def __str__(self):
        return self.bank_name
    
    

class StudentBankDetail(models.Model):
    account_number = models.CharField(max_length=15)
    account_name = models.CharField(max_length=250)
    recipient_code = models.CharField(max_length=200, null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    student=models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.recipient_code