from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post
from .serializer import PostSerializer


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class PostCreateAPIView(CreateAPIView):
#     queryset = Post.objects.all()  # type: ignore
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class PostUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, id=pk, user=request.user)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# class PostUpdateAPIView(UpdateAPIView):
#     queryset = Post.objects.all()  # type: ignore
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return Post.objects.filter(user=self.request.user)  # type: ignore
#
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()  # type: ignore
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)  # type: ignore

    def perform_destroy(self, instance):
        instance.delete()
