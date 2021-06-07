import os
from wsgiref.util import FileWrapper

from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Folder, File, FolderShare, CustomUser, FolderHistory, \
    FileHistory
from .serializers import LoginSerializer, UserSerializer, FolderSerializer, \
    FileSerializer, FolderShareSerializer, FolderHistorySerializer, \
    FileHistorySerializer


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
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


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
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        user_folder = Folder.objects.get(owner=request.user, parent=None)
        return Response(
            {
                "user_data": serializer.data,
                "user_folder": user_folder.id
            }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user,
            data=serializer_data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FolderPropertyView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, pk):
        try:
            folder = Folder.objects.get(
                pk=pk
            )
            data = {
                'number_of_files': folder.files.count(),
                'number_of_folders': folder.children.count(),
            }
            return Response(
                data,
                status=status.HTTP_200_OK
            )
        except File.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class FolderView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request, pk):
        try:
            folder = Folder.objects.create(
                name=request.data.get('folder_name'),
                parent_id=pk,
                owner=request.user
            )
            return Response(
                {
                    'folder': folder.id,
                    'folder_name': folder.name,
                    'folder_owner': folder.owner.id,
                },
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {
                    'status': 'A folder with that name already exists',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, pk):
        try:
            folder = Folder.objects.get(
                pk=pk
            )
            is_folder_share = FolderShare.objects.filter(
                folder_id=pk,
                user_id=request.user.id
            )
            if folder.owner == request.user or is_folder_share:
                FolderHistory.objects.create(
                    folder=folder,
                    user=request.user
                )
                folder_serializer = FolderSerializer(
                    folder.children.all(),
                    many=True
                )
                file_serializer = FileSerializer(
                    folder.files.all(),
                    many=True
                )
                return Response(
                    {
                        'folders': folder_serializer.data,
                        'files': file_serializer.data,
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Folder.DoesNotExist:
            return Response(
                {
                    'response': 'Folder does not exist',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        try:
            folder = Folder.objects.get(
                pk=pk
            )
            folder.delete()
            return Response(
                {
                    'response': f'Folder {folder.name} remove'
                },
                status=status.HTTP_200_OK
            )
        except Folder.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FolderMoveView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def post(self, request):
        folder = Folder.objects.get(
            pk=request.data.get('from_folder')
        )
        folder.parent_id = request.data.get('to_folder')
        folder.save()
        return Response(
            {
                'folder_move_to': folder.path,
            },
            status=status.HTTP_201_CREATED
        )


class FilePropertyView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, pk):
        try:
            file = File.objects.get(
                pk=pk
            )
            serializer = UserSerializer(file.owner)
            data = {
                'size': os.stat(str(file.file)).st_size,
                'owner': serializer.data,
            }
            return Response(
                data,
                status=status.HTTP_200_OK
            )
        except File.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class FileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, pk):
        queryset = File.objects.get(
            id=pk
        )
        FileHistory.objects.create(
            file=queryset,
            user=request.user
        )
        file_handle = queryset.file
        document = open(
            str(file_handle),
            'rb'
        )
        response = HttpResponse(
            FileWrapper(document),
            content_type='whatever'
        )
        response['Content-Disposition'] = f'attachment; ' \
                                          f'filename="{queryset.name}"'
        return response

    def delete(self, request, pk):
        try:
            file = File.objects.get(
                pk=pk
            )
            file.delete()
            return Response(
                {
                    'response': f'File {file.name} remove'
                },
                status=status.HTTP_200_OK
            )
        except Folder.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddFileView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    @parser_classes([MultiPartParser])
    def put(self, request):
        request.data['owner'] = request.user.id
        file_serializer = FileSerializer(
            data=request.data,
        )
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(
                file_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            file_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FileCopyView(APIView):
    def post(self, request):
        try:
            file = File.objects.get(
                pk=request.data.get('file')
            )
            file.duplicate(request.data.get('to_folder'))
            return Response(
                {
                    'file_duplicate_to': request.data.get('to_folder'),
                },
                status=status.HTTP_201_CREATED
            )
        except File.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class ShareFolderView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request, pk):
        if request.user == Folder.objects.get(id=pk).owner:
            folder_members = FolderShareSerializer(
                FolderShare.objects.filter(folder_id=pk), many=True
            )
            return Response(
                {
                    "members": folder_members.data
                }
            )

    def post(self, request, pk):
        if request.user == Folder.objects.get(id=pk).owner:
            user = CustomUser.objects.get(username=request.data.get('username'))
            FolderShare.objects.create(
                folder_id=pk,
                user=user,
            )
            return Response(
                {
                    "response": True
                }
            )
        else:
            return Response(
                {
                    "response": False
                }
            )


class FolderHistoryView(APIView):

    def get(self, request, pk):
        folder_history = FolderHistorySerializer(
            FolderHistory.objects.filter(folder_id=pk), many=True
        )
        return Response(
            {
                "folder_history": folder_history.data
            }
        )
