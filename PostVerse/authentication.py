from django.contrib.auth.models import User

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access')

        if access_token is None:
            return None

        try:
            # Decode the access token
            validated_token = AccessToken(access_token)
        except Exception:
            raise AuthenticationFailed('Invalid token')

        user_id = validated_token['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:   # type: ignore
            raise AuthenticationFailed('User not found')

        return user, None
