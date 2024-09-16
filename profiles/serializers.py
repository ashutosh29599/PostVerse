from rest_framework import serializers

from .models import Profile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'bio', 'photo']
