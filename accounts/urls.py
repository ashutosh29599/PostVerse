from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterUserAPIView, DeleteUserAPIView, ChangePasswordAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('delete-user/', DeleteUserAPIView.as_view(), name='delete_user'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),

    # JWT authentication URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
