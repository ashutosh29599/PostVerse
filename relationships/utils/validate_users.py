from django.contrib.auth.models import User
from functools import wraps
from rest_framework import status
from rest_framework.response import Response


def validate_users(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        if 'follower' not in request.data or 'followed' not in request.data:
            return Response(
                {'detail': 'Both the follower and the followed users\' username or user id must be provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if isinstance(request.data['follower'], str):
            try:
                request.data['follower'] = User.objects.get(username=request.data['follower']).id
            except User.DoesNotExist:  # type: ignore
                return Response(
                    {'detail': 'The follower user does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if isinstance(request.data['followed'], str):
            try:
                request.data['followed'] = User.objects.get(username=request.data['followed']).id
            except User.DoesNotExist:  # type: ignore
                return Response(
                    {'detail': 'The followed user does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return func(self, request, *args, **kwargs)

    return wrapper
