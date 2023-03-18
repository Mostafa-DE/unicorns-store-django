from django.contrib.auth import login
from django.db import transaction
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from users.models import UserProfile
from users.serializer import UserSerializer, UserProfileSerializer


@permission_classes((AllowAny,))
class Login(KnoxLoginView):
    authentication_classes = []

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        knox_response = super(Login, self).post(request, format=None)
        knox_response.set_cookie(
            key='token',
            value=knox_response.data.get('token'),
            httponly=True,
            samesite='none',
            secure=True
        )
        return knox_response


@permission_classes((AllowAny,))
class Register(APIView):
    authentication_classes = []

    @staticmethod
    def post(request):
        username = request.data.get('username')
        email = request.data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise AuthenticationFailed({'email': ['Email already exists']})
        user_serializer = UserSerializer(data=request.data)
        user_profile_serializer = UserProfileSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_profile_serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user_serializer.save()
            user_profile_serializer.save(user=get_user_model().objects.get(username=username))

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


@permission_classes((IsAuthenticated,))
class UserView(APIView):
    @staticmethod
    def get(request):
        try:
            user_id = request.user.id
            user = get_user_model().objects.get(id=user_id)
            if not user:
                raise AuthenticationFailed('Unauthenticated!')

            if not user.is_active:
                raise AuthenticationFailed('User is not active!')

            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class UserProfileView(APIView):
    @staticmethod
    def get(request):
        try:
            user_id = request.user.id
            user_profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        return Response(UserProfileSerializer(user_profile).data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        try:
            user_id = request.user.id
            user_profile = UserProfile.objects.get(user__id=user_id)
            serializer = UserProfileSerializer(instance=user_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile does not exist!'}, status=status.HTTP_404_NOT_FOUND)


@permission_classes((AllowAny,))
class Logout(KnoxLogoutView):
    def post(self, request, format=None):
        username = request.data.get('username')
        if username:
            AuthToken.objects.filter(user__username=username).delete()

        return Response({'success': 'Successfully logged out.'})
