from rest_framework import serializers

from .models import Relationship


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['follower', 'followed', 'created_at']
        read_only_fields = ['created_at']
