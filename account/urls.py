from django.urls import path, include
from account import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'

urlpatterns = [

    
    path('all_users/', views.get_user),
    path('profile/', views.user_detail),
    path('reset_password/', views.reset_password),

    path('<int:user_id>/', views.get_user_detail),
    

    #user login
    path('auth/', views.user_login),
    path('auth/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    
    #social auth 
    # path('auth/social/', include('social_auth.urls'), name="social-login" ),
    
    path('user/forget_password/', include('django_rest_passwordreset.urls', namespace='forget_password')),


]

