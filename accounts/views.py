from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from PostVerse.authentication import CookieJWTAuthentication

from profiles.models import Profile
from .serializers import UserSerializer, UserRegistrationSerializer, ChangePasswordSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_fields'] = {
            'all': self.request.query_params.get('all', 'false'),
            'email': self.request.query_params.get('email', 'true'),
            'date_joined': self.request.query_params.get('date_joined', 'true'),
            'first_name': self.request.query_params.get('first_name', 'true'),
            'last_name': self.request.query_params.get('last_name', 'true'),
            'photo': self.request.query_params.get('photo', 'false'),
        }
        return context

    def get_queryset(self):
        username = self.request.query_params.get('username')
        similar = self.request.query_params.get('similar', 'false')
        sort_by = self.request.query_params.get('sort-by', 'username_asc')

        match sort_by:
            # Sorting by User Model
            case 'username_asc':
                sort_by = 'username'
            case 'username_desc':
                sort_by = '-username'
            case 'oldest_first':
                sort_by = 'date_joined'
            case 'newest_first':
                sort_by = '-date_joined'

            # Sorting by Profile Model
            case 'first_name_asc':
                sort_by = 'profile__first_name'
            case 'first_name_desc':
                sort_by = '-profile__first_name'
            case 'last_name_asc':
                sort_by = 'profile__last_name'
            case 'last_name_desc':
                sort_by = '-profile__last_name'

        queryset = User.objects.all().order_by(sort_by)

        if username:
            if similar == 'false':
                queryset = queryset.filter(username__iexact=username)
            else:
                queryset = queryset.filter(username__contains=username)

        return queryset


class RegisterUserAPIView(APIView):
    authentication_classes = []
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
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            response = Response({"detail": "Login successful"}, status=status.HTTP_200_OK)

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
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response


class CheckAuthAPIView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "Authenticated", "username": request.user.username}, status=status.HTTP_200_OK)


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


class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if not refresh_token:
            return Response({'detail': 'Refresh token cookie not found.'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['refresh'] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                response.set_cookie('access',
                                    response.data.get('access'),
                                    httponly=True,
                                    secure=True,
                                    samesite="Lax")
                response.data.pop('access')
            else:
                response.delete_cookie('access')
                response.delete_cookie('refresh')

            return response
        except (InvalidToken, TokenError):
            return Response({'detail': 'Invalid or expired refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
