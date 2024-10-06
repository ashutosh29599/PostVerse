from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Post
from .serializer import PostSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # the client can set the page size via query param
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    """
    Issue: Currently any authenticated user can update any post (even those that they don't own).
    """
    queryset = Post.objects.all()  # type: ignore
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        username = self.request.query_params.get('username')
        sort_by = self.request.query_params.get('sort-by', '-created_at')

        # select_related helps us add the 'user' in the response
        queryset = Post.objects.select_related('user').order_by(sort_by)  # type: ignore

        if username:
            queryset = queryset.filter(user__username=username)

        return queryset

    def create(self, request, *args, **kwargs):
        if 'text' not in request.data and 'photo' not in request.data:
            return Response(
                {'detail': 'A post must either have text or photo or both'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # TODO: Check the request.user == user making this request.
        # Need to send the user_id/username/email/your choice of identifier in the data.
        # request.user.id, request.user, request.user.username (same as prev), request.user.email all work.

        if 'text' not in request.data and 'photo' not in request.data:
            return Response(
                {'detail': 'A post must either have text or photo or both.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# class PostCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             post = serializer.save(user=request.user)
#             return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# #
# # class PostCreateAPIView(CreateAPIView):
# #     queryset = Post.objects.all()  # type: ignore
# #     serializer_class = PostSerializer
# #     permission_classes = [IsAuthenticated]
# #
# #     def perform_create(self, serializer):
# #         serializer.save(user=self.request.user)
#
#
# class PostUpdateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def put(self, request, pk, *args, **kwargs):
#         post = get_object_or_404(Post, id=pk, user=request.user)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             post = serializer.save(user=request.user)
#             return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# #
# # class PostUpdateAPIView(UpdateAPIView):
# #     queryset = Post.objects.all()  # type: ignore
# #     serializer_class = PostSerializer
# #     permission_classes = [IsAuthenticated]
# #
# #     def get_queryset(self):
# #         return Post.objects.filter(user=self.request.user)  # type: ignore
# #
# #     def perform_update(self, serializer):
# #         serializer.save(user=self.request.user)
#
#
# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()  # type: ignore
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Post.objects.filter(user=self.request.user)  # type: ignore
#
#     def perform_destroy(self, instance):
#         instance.delete()
