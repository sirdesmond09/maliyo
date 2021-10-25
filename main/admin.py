from django.contrib import admin
from .models import Bank, StudentBankDetail
# Register your models here.
admin.site.register([Bank, StudentBankDetail])