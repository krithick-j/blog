from rest_framework import viewsets
from .models import Article, Comment, User
from .serializers import ArticleSerializer, CommentSerializer, UserSerializer
from .permissions import IsOwner, IsAdmin, IsMember


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            # Only superusers can create users
            return [IsAdmin()]
        elif self.action in ['update', 'destroy']:
            # Owners or superusers can update or delete users
            return [IsOwner() | IsAdmin()]
        return []  # No special permissions for listing or retrieving users

    def perform_create(self, serializer):
        # Check if this is the first user being created
        if User.objects.count() == 0:
            # Set the first user as the Owner
            serializer.save(is_owner=True)
        else:
            # For all other users, set is_owner as False
            serializer.save(is_owner=False)
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdmin()]
        return [IsMember()]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsMember()]
        return [IsMember()]
