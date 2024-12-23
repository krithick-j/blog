from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ArticleViewSet, CommentViewSet, FeatureFlagViewSet, UserViewSet

# Create a router for viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)  # Registering the UserViewSet to handle user-related requests
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'feature-flags', FeatureFlagViewSet, basename='feature-flag')

urlpatterns = [
    # JWT Token endpoints for authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Include the routes for the viewsets defined in the router
    path('', include(router.urls)),
]
