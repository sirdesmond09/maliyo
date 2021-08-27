from django.contrib import admin
from .models import OTP, Student
# Register your models here.
admin.site.register([OTP, Student])