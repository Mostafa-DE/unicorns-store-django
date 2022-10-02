from django.contrib.auth import login, logout
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, UserProfile
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
        user_serializer = UserSerializer(data=request.data)
        user_profile_serializer = UserProfileSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_profile_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        user_profile_serializer.save(user=User.objects.get(username=request.data.get('username')))
        return Response(user_serializer.data, status=201)


@permission_classes((IsAuthenticated,))
class UserView(APIView):

    @staticmethod
    def get(request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if not user:
            raise AuthenticationFailed('Unauthenticated!')

        if not user.is_active:
            raise AuthenticationFailed('User is not active!')

        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


@permission_classes((IsAuthenticated,))
class UserProfileView(APIView):
    @staticmethod
    def get(request):
        try:
            user_id = request.user.id
            user_profile = UserProfile.objects.get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile does not exist!'}, status=404)

        return Response(UserProfileSerializer(user_profile).data, status=200)

    @staticmethod
    def put(request):
        try:
            user_id = request.user.id
            user_profile = UserProfile.objects.get(user__id=user_id)
            serializer = UserProfileSerializer(instance=user_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile does not exist!'}, status=404)


@permission_classes((AllowAny,))
class Logout(KnoxLogoutView):

    def post(self, request, format=None):
        logout(request)
        response = Response()
        response.delete_cookie(key='token', samesite='none')
        response.delete_cookie(key='csrftoken', samesite='none')
        return response
