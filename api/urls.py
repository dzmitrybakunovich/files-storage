from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('user/signup/', views.UserRegistration.as_view(), name='signup'),
    path('user/jwt/', views.UserLogin.as_view(), name='login'),
    path('user/', views.UserProfile.as_view(), name='profile'),
]
