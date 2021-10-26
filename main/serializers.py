from config import settings
from rest_framework import serializers
from .models import Attendance, Bank, batch_date, StudentBankDetail
import requests, os, pyotp
from .helpers.verify_bank import bank_verification
from django.core.mail import send_mail
 
# function to generate OTP
 

class StudentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    class Meta:
        fields = ('file',)
        
        
# class EmailVerifySerializer(serializers.Serializer):
#     email = serializers.EmailField()
    
    
#     def verify_email(self):
#         email = self.validated_data['email']
        
#         if Student.objects.filter(email=email, batch=batch_date(), is_active=True).exists():
#             student = Student.objects.get(email=email, batch=batch_date(), is_active=True)
#             serializer = StudentSerializer(student)
#             if student.is_verified == False:
                
#                 code = get_otp()
                
#                 subject = "COMPLETE YOUR VERIFICATION ON MALIYO"
                
#                 message = f"""Hi, {student.name}!
# Kindly complete your verification on the maliyo games portal with the OTP below:

#                 {code}        

# Expires in 60 seconds!

# Thank you,
# Maliyo Games.                
# """
#                 email_from = settings.Common.DEFAULT_FROM_EMAIL
#                 recipient_list = [email]
#                 send_mail( subject, message, email_from, recipient_list)
                
#                 OTP.objects.create(code=code, student=student)
#                 return {'message': 'Please check your email for OTP.', 'data':serializer.data}
            
#             else:
#                 raise serializers.ValidationError(detail='Student with this email has been verified before.')
                
        
#         else:
#             raise serializers.ValidationError(detail='Student with this email not found. Plese check that the email is correct',)
            
            
# class OTPVerifySerializer(serializers.Serializer):
#     otp = serializers.CharField(max_length=6)
    
    
#     def verify_otp(self):
#         otp = self.validated_data['otp']
        
#         if len(otp) == 6 and OTP.objects.filter(code=otp).exists():
#             otp = OTP.objects.get(code=otp)
            
#             if totp.verify(otp):
#                 if otp.student.is_verified == False:
#                     otp.student.is_verified=True
#                     otp.student.save()
                    
#                     #clear all otp for this student after verification
#                     all_otps = OTP.objects.filter(student=otp.student)
#                     all_otps.delete()
                    
#                     serializer = StudentSerializer(otp.student)
#                     return {'message': 'Verification Complete', 'data':serializer.data}
#                 else:
#                     raise serializers.ValidationError(detail='Student with this otp has been verified before.')
            
                
#             else:
#                 raise serializers.ValidationError(detail='OTP expired')
                    
        
#         else:
#             raise serializers.ValidationError(detail='Invalid OTP')
        

class BankSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bank
        fields = '__all__'
        
        
class StudentBankVerificationSerializer(serializers.Serializer):
    account_num =serializers.CharField(max_length=250)
    bank_id = serializers.IntegerField()
    student_id = serializers.IntegerField()
    
    
    
    def verify_bank_details(self):
        try:
            bank = Bank.objects.get(id=self.validated_data['bank_id'])
        except Bank.DoesNotExist:
            raise serializers.ValidationError(detail=f"Bank with id {self.validated_data['bank_id']} not found")
        
        
        data = bank_verification(code = bank.paystack_code, account_num=self.validated_data['account_num'])
        data['bank'] = bank.bank_name
        data['bank_id'] = bank.id
        
        return data
    
class StudentBankDetailSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField()
    bank_name = serializers.ReadOnlyField()
    
    class Meta:
        model = StudentBankDetail
        fields = ['account_number', 'account_name', 'recipient_code', 'bank', 'student', 'student_name', 'bank_name', 'date_added']
        
    
    def add_recepient(self, request):
        if 'student' in self.validated_data.keys():
            self.validated_data.pop('student')
            
        res = requests.post(
            url = 'https://api.paystack.co/transferrecipient', 
            data= { "type": "nuban", 
                "name": self.validated_data["account_name"], 
                "account_number": self.validated_data["account_number"], 
                "bank_code": self.validated_data["bank"].paystack_code, 
                "currency": "NGN"
                },
                        
            headers={
                'Authorization':f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"
        })
        
        if res.json()['status'] == True:
            print(res.json()['data'])
            recipient_code = res.json()['data']['recipient_code'] 
            data = StudentBankDetail.objects.create(**self.validated_data, recipient_code=recipient_code, student=request.user)
            return data
        else:
            raise serializers.ValidationError(detail='Unable to add account details')
        
        
class AttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields = '__all__'
        