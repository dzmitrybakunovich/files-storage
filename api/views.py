from django.db import IntegrityError

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import LoginSerializer, UserSerializer
from .models import Folder


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            status_code = status.HTTP_201_CREATED
            data = {
                'status code': status_code,
                'response': 'User created successfully',
                'username': serializer.data['username']
            }
            return Response(data, status=status_code)
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(serializer.errors, status=status_code)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            status_code = status.HTTP_200_OK
            data = {
                'status code': status_code,
                'response': 'User logged in successfully',
                'token': serializer.data['token'],
            }
            return Response(data, status=status_code)
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(serializer.errors, status=status_code)


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(serializer.errors, status=status_code)


class FolderView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        folder = Folder(
            name=request.data.get('folder_name'),
            parent_id=request.data.get('parent_id'),
            owner=request.user
        )
        try:
            folder.save()
            return Response(
                {
                    'folder_id': folder.id,
                    'folder_name': folder.name,
                    'folder_owner': folder.owner.id,
                }
            )
        except IntegrityError:
            return Response(
                {
                    'status': 'A folder with that name already exists',
                }
            )

    # def get(self, request):
    #     if os.path.exists(full_path):
    #         data = {
    #             'success': True,
    #             'listdir': os.listdir(full_path)
    #         }
    #         return Response(data, status=status.HTTP_200_OK)
    #     else:
    #         data = {
    #             'success': False
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)
