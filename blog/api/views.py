from rest_framework import viewsets
from .models import Article, Comment, User
from .serializers import ArticleSerializer, CommentSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin, IsAdmin, IsMember
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone (authenticated or unauthenticated) to create a user
            return []
        return [IsAuthenticated()]  # Require authentication for other actions (update, delete)

    def perform_create(self, serializer):
        # Automatically set the role for the first user
        if User.objects.count() == 0:
            serializer.save(role='owner')  # First user is the owner
        else:
            # If the user is unauthenticated, set the role as 'member'
            if not self.request.user.is_authenticated:
                serializer.save(role='member')  # Set role as member if unauthenticated
            else:
                # If authenticated, keep the default role as 'member'
                serializer.save(role='member')

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdmin()]  # Only admin can create/edit/delete articles
        return [IsMember()]  # All authenticated users (members) can view articles

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set the current user as the author of the article


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsMember()]  # Members can add comments
        return [IsMember()]  # All authenticated users can view comments

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Set the current user as the comment author
