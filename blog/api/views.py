from django.http import JsonResponse
from rest_framework import viewsets
from .models import Article, Comment, FeatureFlag, User
from .serializers import ArticleSerializer, CommentSerializer, FeatureFlagSerializer, UserSerializer
from .permissions import IsAdmin, IsMember
from rest_framework.permissions import IsAuthenticated, AllowAny
from .decorators import feature_flag_enabled

from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Only admins or owners can create users, while others must be authenticated to update or delete
        if self.action == 'create':
            return []  # Anyone can create (authenticated or unauthenticated)
        return [IsAuthenticated()]  # Require authentication for update and delete actions

    def perform_create(self, serializer):
        # Check if the user is the first user
        if User.objects.count() == 0:
            # Automatically set the role for the first user as 'owner'
            serializer.save(role='owner')
        else:
            # For authenticated users, allow them to assign a role in the payload if they're an admin or owner
            if self.request.user.is_authenticated:
                if self.request.user.role in ['admin', 'owner']:  # If logged-in user is admin or owner
                    # Use the role from the payload, if provided
                    role = self.request.data.get('role', 'member')  # Default to 'member' if no role provided
                    serializer.save(role=role)
                else:
                    # If the authenticated user is not admin/owner, set the default role as 'member'
                    serializer.save(role='member')
            else:
                # If the user is unauthenticated, set the role as 'member'
                serializer.save(role='member')

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        # Allow admins to create, update, delete; members can view only
        if self.request.method in ['POST', 'PUT', 'PATCH', 'GET', 'DELETE']:
            return [IsAdmin()]
        return [IsAuthenticated()]  # Allow authenticated users to view articles

    @feature_flag_enabled("manage_article_permissions")
    def perform_create(self, serializer):
        print(f"Feature flag 'manage_article_permissions' is enabled.")  # Debugging line

        # Automatically set the authenticated user as the author
        serializer.save(author=self.request.user)


# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     def get_permissions(self):
#         # Allow admins to create, update, delete; members can view only
#         if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
#             return [IsAdmin()]
#         return [IsAuthenticated()]  # Allow authenticated users to view articles

#     def perform_create(self, serializer):
#         # Automatically set the authenticated user as the author
#         serializer.save(author=self.request.user)
        
#     @feature_flag_enabled("manage_article_permissions")
#     def perform_update(self, serializer):
#         # Logic for updating an article
#         serializer.save()

#     @feature_flag_enabled("manage_article_permissions")
#     def perform_destroy(self, instance):
#         # Logic for deleting an article
#         instance.delete()

#     def list(self, request, *args, **kwargs):
#         # This action could be unrestricted or protected by feature flags
#         return super().list(request, *args, **kwargs)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        
        if self.request.method in ['POST', 'PUT', 'PATCH', 'GET', 'DELETE']:
            return [IsAuthenticated()]  # Only authenticated users can add/edit comments
        return []
    
    def perform_create(self, serializer):
        # Automatically set the authenticated user as the author
        serializer.save(author=self.request.user)
        
class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer
