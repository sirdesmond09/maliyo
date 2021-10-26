from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance, Bank, StudentBankDetail, User, batch_date
from .serializers import AttendanceSerializer, BankSerializer, StudentBankDetailSerializer, StudentBankVerificationSerializer, StudentUploadSerializer
from drf_yasg.utils import swagger_auto_schema
from .helpers import upload
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import csv

from django.http import HttpResponse
from datetime import datetime



# @swagger_auto_schema(methods=['POST'], request_body=EmailVerifySerializer())
# @api_view(['POST'])
# def email_verification(request):
    
#     """Api view for verifying emails """

#     if request.method == 'POST':

#         serializer = EmailVerifySerializer(data = request.data)

#         if serializer.is_valid():
#             data = serializer.verify_email()
            
#             return Response(data, status=status.HTTP_200_OK)
#         else:

#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        

# @swagger_auto_schema(methods=['POST'], request_body=OTPVerifySerializer())
# @api_view(['POST'])
# def otp_verification(request):
    
#     """Api view for verifying OTPs """

#     if request.method == 'POST':

#         serializer = OTPVerifySerializer(data = request.data)

#         if serializer.is_valid():
#             data = serializer.verify_otp()
            
#             return Response(data, status=status.HTTP_200_OK)
#         else:

#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        

@swagger_auto_schema(methods=['POST'], request_body=StudentUploadSerializer())
@api_view(['POST'])
def upload_students(request):



    if request.method == 'POST':

        serializer = StudentUploadSerializer(data = request.data)


        if serializer.is_valid():

            file = serializer.validated_data['file']
            try:

                rows = upload.process_data(file)
            except Exception:
                data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'errors'  : ["Error uploading file.\n Please check that data is correct."]

                }
                return Response(data, status = status.HTTP_400_BAD_REQUEST)
            
            success = False
            users = []
            for row in rows:
                success = False
                try:

                    users.append(User(**row, is_active=True))

                    success = True
                except Exception:
                    success = False
                    
            if success == True:
                User.objects.bulk_create(users)
                data = {
                    'status'  : True,
                    'message' : "File upload successful",

                }

                return Response(data, status = status.HTTP_200_OK)
            else:
                data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'errors'  : ["Error uploading file.\n Please check that data is correct"]

            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'errors'  : serializer.errors

            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        
        
        

@api_view(['GET'])
def get_banks(request):
    if request.method=='GET':
        banks = Bank.objects.all()
        
        serializer = BankSerializer(banks, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        

@swagger_auto_schema(methods=['POST'], request_body=StudentBankVerificationSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def bank_verification(request):
    
    """Api view for verifying bank accounts """

    if request.method == 'POST':

        serializer = StudentBankVerificationSerializer(data = request.data)

        if serializer.is_valid():
            if StudentBankDetail.objects.filter(student=request.user, month=batch_date, is_active=True).exists():
                raise ValidationError(detail="Bank details already verified for this month. Please wait till next month.")
            
            data = serializer.verify_bank_details()
            
            return Response(data, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        
@swagger_auto_schema(methods=['POST'], request_body=StudentBankDetailSerializer())
@api_view(['POST'])
def bank_details(request):
    
    """Api view for verifying bank accounts """

    if request.method == 'POST':

        serializer = StudentBankDetailSerializer(data = request.data)

        if serializer.is_valid():
            data = serializer.add_recepient()
            serializer = StudentBankDetailSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
def all_bank_details(request):
    """Api view to get all the account details of all verified students!"""
    
    obj = StudentBankDetail.objects.filter(is_active=True)
    serializer = StudentBankDetailSerializer(obj, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def download_bank_details(request):
    """Api view to download the bank details as csv"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bank_details.csv"'

    writer = csv.writer(response)
    
    writer.writerow([
            's/n',
            'account_number',
            'account_name',
            'recipient_code',
            'bank_name',
            'student_name',
            'date_added'
        ])
    
    count = 0
    for bank in StudentBankDetail.objects.filter(month=batch_date):
        count +=1
        writer.writerow([
            count,
            str(bank.account_number),
            str(bank.account_name),
            str(bank.recipient_code),
            str(bank.bank.bank_name),
            str(bank.student.name),
            datetime.strftime(bank.date_added, '%d-%m-%Y')
        ])
        


    return response
    
    
@swagger_auto_schema(methods=['POST'], request_body=AttendanceSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_attendance(request):
    if request.method=='POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')
                
            Attendance.objects.create(**serializer.validated_data, user=request.user)
            
            return Response({"message":'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_records(request):
    
    obj = Attendance.objects.filter(is_active=True, user=request.user)
    serializer = AttendanceSerializer(obj, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
    