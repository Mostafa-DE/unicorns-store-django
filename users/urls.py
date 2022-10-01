from django.urls import path
from users.views import Login, Logout, Register, UserView, UserProfileView

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='knox_login'),
    path('user/', UserView.as_view(), name='user'),
    path('user-profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', Logout.as_view(), name='knox_logout'),
]
