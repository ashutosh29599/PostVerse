from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import PostCreateAPIView, PostUpdateAPIView, PostDeleteAPIView
from .views import PostViewSet

# urlpatterns = [
#     path('create/', PostCreateAPIView.as_view(), name='post_create'),
#     path('<int:pk>/update/', PostUpdateAPIView.as_view(), name='post_update'),
#     path('<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post_delete'),
# ]

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls))
]
