from account.serializers import UserSerializer
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from config import settings
from rest_framework import serializers
from django.template.loader import render_to_string
   

User = get_user_model()

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    token = "https://www.edm.com/forgot-password/{}".format(reset_password_token.key)
    
    msg_html = render_to_string('forgot_password.html', {
                        'first_name': str(reset_password_token.user.first_name).title(),
                        'token':token})
    
    message= 'Hello {},\n\nYou are receiving this message because you or someone else have requested the reset of the password for your account.\nPlease click on the following link, or paste this into your browser to complete the process within 24hours of receiving it:\n{}\n\nPlease if you did not request this please ignore this e-mail and your password would remain unchanged.\n\nRegards,\nEDM Support'.format(reset_password_token.user.first_name, token)
    
    send_mail(
        subject = "RESET PASSWORD FOR EDM PORTAL",
        message= message,
        html_message=msg_html,
        from_email  = 'EDM SUPPORT <noreply@ecomap.ng>',
        recipient_list= [reset_password_token.user.email]
    )
    

@receiver(post_save, sender=User)
def notify_user(sender, instance, created, **kwargs):
    if created:
        subject = "YOUR ACCOUT IS READY FOR USE"
        
        message = f"""Hi, {str(instance.first_name).title()}.
Thank you for signing up for the AWS fundamental training. Kindly find your login details below:
                {instance.email}
                {instance.password}        
Follow this link to login: https://ucheckin.univelcity.com/
Thank you,
Support Team                
"""   
        msg_html = render_to_string('signup_email.html', {
                        'first_name': str(instance.first_name).title(),
                        'email':instance.email,
                        'password':instance.password})
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
    
    
    

  