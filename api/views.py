from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, LoginSerializer


class UserRegistration(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            status_code = status.HTTP_201_CREATED
            data = {
                'status code': status_code,
                'response': 'User created successfully',
                'username': user.username,
                'email': user.email,
            }
            return Response(data, status=status_code)
        data = serializer.errors
        return Response(data)


class UserLogin(APIView):
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
        data = serializer.errors
        return Response(data)
