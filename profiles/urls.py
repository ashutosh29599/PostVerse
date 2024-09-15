from django.urls import path

from .views import UserProfileAPIView, EditUserProfileAPIView

urlpatterns = [
    path('profile/<str:username>/', UserProfileAPIView.as_view(), name='profile'),
    path('edit-profile/', EditUserProfileAPIView.as_view(), name='edit_profile'),
]
