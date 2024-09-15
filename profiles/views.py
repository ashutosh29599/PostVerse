from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Profile
from .serializers import UserProfileSerializer


class UserProfileAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(Profile, user__username=username)


class EditUserProfileAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        user = self.request.data.get('user')
        return get_object_or_404(Profile, user=user)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
