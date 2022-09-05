from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'created',
            'updated',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'error_messages': {'required': 'Password is required'}},
            'username': {'required': True, 'error_messages': {'required': 'Username is required'}},
            'email': {'required': True, 'error_messages': {'required': 'Email is required'}},
            'first_name': {
                'required': True,
                'allow_blank': False,
                'error_messages': {'error': 'First name is required'}
            },
            'last_name': {'required': True, 'allow_blank': False, 'error_messages': {'error': 'Last name is required'}},
            'is_active': {'read_only': True},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
