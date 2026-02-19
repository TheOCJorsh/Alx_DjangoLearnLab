from django.urls import path
from .views import FeedView
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet


urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', like_post, name='like-post'),
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike-post'),
    
]

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
