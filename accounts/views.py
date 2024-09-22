from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.db import IntegrityError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from PostVerse.authentication import CookieJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from profiles.models import Profile
from .serializers import UserRegistrationSerializer, ChangePasswordSerializer


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(user=user)  # type: ignore
            login(request, user)

            return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({"detail": "Login successful."}, status=status.HTTP_200_OK)

            # secure=True for prod
            response.set_cookie("access",
                                str(refresh.access_token),  # type: ignore
                                httponly=True,
                                secure=True,
                                samesite="None"
                                )
            response.set_cookie("refresh",
                                str(refresh),
                                httponly=True,
                                secure=True,
                                samesite="None"
                                )

            return response
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response


class CheckAuthAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "Authenticated", "username": request.user.username}, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # updated_response = Response({"message": "Token refreshed successfully", status: status.HTTP_200_OK})
            response.set_cookie('access',
                                response.data.get('access'),
                                httponly=True,
                                secure=True,
                                samesite="Lax")
            response.set_cookie('refresh',
                                response.data.get('refresh'),
                                httponly=True,
                                secure=True,
                                samesite="Lax")
            return response

        return response


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
