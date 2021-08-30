from rest_framework import serializers
from .models import Bank, Student, batch_date, OTP, StudentBankDetail
import math, random, requests, os
from .helpers.verify_bank import bank_verification
 
# function to generate OTP

def generate_otp() :
 
    digits = "0123456789"
    code = ""

    for i in range(6) :
        code += digits[math.floor(random.random() * 10)]
 
    return code

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = '__all__'
        
        

class StudentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    class Meta:
        fields = ('file',)
        
        
class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
    def verify_email(self):
        email = self.validated_data['email']
        
        if Student.objects.filter(email=email, batch=batch_date(), is_active=True).exists():
            student = Student.objects.get(email=email, batch=batch_date(), is_active=True)
            
            if student.is_verified == False:
                code = generate_otp()
                print(code)
                OTP.objects.create(code=code, student=student)
                return {'message': 'Please check your email for OTP.'}
            
            else:
                raise serializers.ValidationError(detail='Student with this email has been verified before.')
                
        
        else:
            raise serializers.ValidationError(detail='Student with this email not found. Plese check that the email is correct',)
            
            
class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    
    
    def verify_otp(self):
        otp = self.validated_data['otp']
        
        if len(otp) == 6 and OTP.objects.filter(code=otp).exists():
            otp = OTP.objects.get(code=otp)
            
            if otp.expired():
            
                raise serializers.ValidationError(detail='OTP expired')
            else:
                if otp.student.is_verified == False:
                    otp.student.is_verified=True
                    otp.student.save()
                    serializer = StudentSerializer(otp.student)
                    return {'message': 'Verification Complete', 'data':serializer.data}
                else:
                    raise serializers.ValidationError(detail='Student with this otp has been verified before.')
                    
        
        else:
            raise serializers.ValidationError(detail='Invalid OTP')
        

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
            student = Student.objects.get(id=self.validated_data['student_id'], batch=batch_date(), is_verified=True)
        except Bank.DoesNotExist:
            raise serializers.ValidationError(detail=f"Bank with id {self.validated_data['bank_id']} not found")
        except Student.DoesNotExist:
            raise serializers.ValidationError(detail=f"Student for batch {batch_date()} with id {self.validated_data['student_id']} not found")
        
        data = bank_verification(code = bank.paystack_code, account_num=self.validated_data['account_num'])
        data['bank'] = bank.bank_name
        data['bank_id'] = bank.id
        data['student_id'] = student.id
        
        return data
    
class StudentBankDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudentBankDetail
        fields = '__all__'
        
    
    def add_recepient(self):
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
            data = StudentBankDetail.objects.create(**self.validated_data, recipient_code=recipient_code)
            return data
        else:
            raise serializers.ValidationError(detail='Unable to add account details')