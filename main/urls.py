from django.urls import path
from . import views


urlpatterns = [
    path('students/email_verification/', views.email_verification),
    path('students/otp_verification/', views.otp_verification),
    path('students/bank_verification/', views.bank_verification),
    path('students/save_bank_details/', views.bank_details),
    path('students/upload/', views.upload_students),
    path('banks/', views.get_banks)

]
