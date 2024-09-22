from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterUserAPIView, LoginUserAPIView, CheckAuthAPIView, CustomTokenRefreshView, DeleteUserAPIView, \
    ChangePasswordAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('check-auth/', CheckAuthAPIView.as_view(), name='check_auth'),
    path('delete-user/', DeleteUserAPIView.as_view(), name='delete_user'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),

    # JWT authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh')
]
