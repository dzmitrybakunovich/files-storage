from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('user/signup/', views.UserRegistrationView.as_view(), name='signup'),
    path('user/jwt/', views.UserLoginView.as_view(), name='login'),
    path('user/', views.UserProfileView.as_view(), name='profile'),
    path('folder/<int:pk>', views.FolderView.as_view(), name='folder'),
    path('folder/<int:pk>/property', views.FolderPropertyView.as_view(),
         name='folder_property'),
    path('folder/<int:pk>/history', views.FolderHistoryView.as_view(), name='folder'),
    path('folder/move/', views.FolderMoveView.as_view(), name='move_folder'),
    path('folder/share/<int:pk>', views.ShareFolderView.as_view(),
         name='share_folder'),
    path('file/<int:pk>/', views.FileView.as_view(), name='folder'),
    path('file/<int:pk>/property', views.FilePropertyView.as_view(),
         name='file_property'),
    path('file/add/', views.AddFileView.as_view(), name='file_add'),
    path('file/copy/', views.FileCopyView.as_view(), name='copy_file'),
]
