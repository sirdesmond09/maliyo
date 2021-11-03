from django.urls import path
from . import views


urlpatterns = [
    # path('students/email_verification/', views.email_verification),
    # path('students/otp_verification/', views.otp_verification),
    path('students/bank_verification/', views.bank_verification),
    path('students/save_bank_details/', views.bank_details),
    path('students/upload/', views.upload_students),
    path('students/download/', views.download_bank_details),
    path('students/bank_details/', views.all_bank_details),
    path('banks/', views.get_banks),
    path('students/clockins/', views.add_attendance),
    path('students/my_clockins/', views.get_records),
    path('students/activities/<int:user_id>/', views.user_record),

]
