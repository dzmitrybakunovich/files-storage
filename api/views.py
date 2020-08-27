from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class UserRegistration(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data = {
                'response': 'User created successfully.',
                'username': user.username,
                'email': user.email,
            }
        else:
            data = serializer.errors
        return Response(data)
