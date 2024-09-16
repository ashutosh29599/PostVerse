from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, update_session_auth_hash
from django.db import IntegrityError

from profiles.models import Profile
from .serializers import UserRegistrationSerializer, ChangePasswordSerializer


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)   # type: ignore
            login(request, user)

            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        try:
            user.delete()
            return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except IntegrityError:
            return Response({"detail": "An error occurred while trying to delete the user."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                raise ValidationError({'old_password': 'Your old password is incorrect.'})

            user.set_password(serializer.validated_data['new_password1'])
            user.save()

            # Update the session so the user doesn't get logged out
            update_session_auth_hash(request, user)

            return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
