from rest_framework import serializers
from .models import User, UserProfile


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

    def create(self, data):
        password = data.pop('password', None)
        instance = self.Meta.model(**data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'phone',
            'address',
            'city',
            'building_number',
            'created',
            'updated',
        ]
        extra_kwargs = {
            'user': {'read_only': True, 'required': True, 'error_messages': {'required': 'User is required'}},
            'created': {'read_only': True},
            'updated': {'read_only': True},
        }

    def create(self, data):
        instance = self.Meta.model(**data)
        instance.save()
        return instance

    def update(self, instance, data):
        instance.phone = data.get('phone', instance.phone)
        instance.address = data.get('address', instance.address)
        instance.city = data.get('city', instance.city)
        instance.building_number = data.get('building_number', instance.building_number)
        instance.save()
        return instance
