from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


AUTH_PROVIDERS = {'facebook': 'facebook', 
                  'google': 'google',  
                  'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
    first_name          = models.CharField(_('first name'),max_length = 250)
    last_name          = models.CharField(_('last name'),max_length = 250)
    email         = models.EmailField(_('email'), unique=True)
    phone         = models.CharField(_('phone'), max_length = 20)
    date_of_birth         = models.CharField(_('date_of_birth'), max_length = 20)
    gender         = models.CharField(_('gender'), max_length = 20)
    nationality         = models.CharField(_('nationality'), max_length = 100)
    address         = models.CharField(_('address'), max_length = 400)
    state_of_residence         = models.CharField(_('state_of_residence'), max_length = 100)
    education         = models.CharField(_('education'), max_length = 400)
    course         = models.CharField(_('course'), max_length = 400)
    currently_working         = models.CharField(_('currently_working'), max_length=20)
    programing_experience         = models.CharField(_('programing_experience'), max_length = 400)
    own_laptop         = models.CharField(_('own_laptop'), max_length=20)
    how_did_you_hear_about_us         = models.CharField(_('how_did_you_hear_about_us'), max_length=400, blank=True, null=True)
    password      = models.CharField(_('password'), max_length=500)
    uploaded_id_url = models.CharField(_('ID url'), max_length = 300, null=True)
    is_active     = models.BooleanField(_('active'), default=True)
    is_staff     = models.BooleanField(_('staff'), default=False)
    is_admin    = models.BooleanField(_('admin'), default=False)
    is_superuser    = models.BooleanField(_('superuser'), default=False)
    date_joined   = models.DateTimeField(_('date joined'), auto_now_add=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
    
    
    