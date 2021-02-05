from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('user/signup/', views.UserRegistrationView.as_view(), name='signup'),
    path('user/jwt/', views.UserLoginView.as_view(), name='login'),
    path('user/', views.UserProfileView.as_view(), name='profile'),
    path('folder/', views.FolderView.as_view(), name='folder'),
    path('folder/move', views.FolderMoveView.as_view(), name='move_folder'),
]
