from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='profile.first_name', read_only=True)
    last_name = serializers.CharField(source='profile.last_name', read_only=True)
    photo = serializers.ImageField(source='profile.photo', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'date_joined', 'first_name', 'last_name', 'photo']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        include_fields = self.context.get('include_fields')
        representation['username'] = instance.username

        include_all_fields = True if include_fields.get('all', 'false').lower() == 'true' else False

        if not include_all_fields:
            if include_fields.get('email', 'true').lower() == 'false':
                representation.pop('email', None)

            if include_fields.get('date_joined', 'true').lower() == 'false':
                representation.pop('date_joined', None)

            if include_fields.get('first_name', 'true').lower() == 'false':
                representation.pop('first_name', None)

            if include_fields.get('last_name', 'true').lower() == 'false':
                representation.pop('last_name', None)

            if include_fields.get('photo', 'true').lower() == 'false':
                representation.pop('photo', None)

        return representation


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )  # this is a tuple -- we are using a built-in model.

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password1'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):  # noqa
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "Passwords do not match."})

        validate_password(data['new_password1'])
        return data
