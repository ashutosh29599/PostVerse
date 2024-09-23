from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (RegisterUserAPIView,
                    LoginUserAPIView,
                    LogoutUserAPIView,
                    CheckAuthAPIView,
                    CustomTokenRefreshView,
                    DeleteUserAPIView,
                    ChangePasswordAPIView)

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('check-auth/', CheckAuthAPIView.as_view(), name='check_auth'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('delete-user/', DeleteUserAPIView.as_view(), name='delete_user'),

    # JWT authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),    # To be deprecated
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh')
]
