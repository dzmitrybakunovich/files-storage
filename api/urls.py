from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path(
        'registration/',
        views.UserRegistration.as_view(),
        name='registration'
    ),
    path('login/', views.UserLogin.as_view(), name='login'),
]
