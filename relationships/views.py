from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Relationship
from .serializer import RelationshipSerializer
from .utils.validate_users import validate_users


class RelationshipViewSet(viewsets.ModelViewSet):
    # TODO: Currently any authenticated user can delete any relationship. Users should be able to delete a
    # TODO: relationship in which they are either the followed or the follower.

    queryset = Relationship.objects.all()  # type: ignore
    serializer_class = RelationshipSerializer

    # def get_queryset(self):
    #     queryset = Relationship.objects.all()  # type: ignore
    #
    #     return queryset

    @validate_users
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['DELETE'], url_path='delete-relationship')
    @validate_users
    def destroy_relationship(self, request, *args, **kwargs):
        try:
            relationship = Relationship.objects.get(  # type: ignore
                follower=request.data['follower'],
                followed=request.data['followed']
            )
        except Relationship.DoesNotExist:  # type: ignore
            return Response(
                {'detail': 'This relationship does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        relationship.delete()

        return Response(
            {'detail': 'Relationship deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )
