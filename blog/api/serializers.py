from rest_framework import serializers
from .models import Article, Comment, User

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_owner', 'is_admin', 'is_member']
        read_only_fields = ['is_owner']  # Prevent is_owner from being included in input
