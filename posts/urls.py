from django.urls import path

from .views import PostCreateAPIView, PostUpdateAPIView, PostDeleteAPIView

urlpatterns = [
    path('create/', PostCreateAPIView.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdateAPIView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post_delete'),
]
