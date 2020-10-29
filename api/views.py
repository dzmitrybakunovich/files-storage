from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import LoginSerializer, UserSerializer


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
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        status_code = status.HTTP_400_BAD_REQUEST
        return Response(serializer.errors, status=status_code)
