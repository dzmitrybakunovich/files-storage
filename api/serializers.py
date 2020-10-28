from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import CustomUser

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exists'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'password',
            'password2',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'}
            )
        user.create_path()
        user.set_password(password)
        user.save()
        return user
