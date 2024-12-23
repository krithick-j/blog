from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Display username instead of ID
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'tags', 'author', 'created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display username instead of ID
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())  # ForeignKey to Article

    class Meta:
        model = Comment
        fields = ['id', 'article', 'user', 'content', 'created_at']




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password is write-only
        }

    def create(self, validated_data):
        # Automatically set the role for the first user
        if User.objects.count() == 0:
            validated_data['role'] = 'owner'  # First user is the owner
        else:
            # Set the role to member if no role is provided
            validated_data['role'] = validated_data.get('role', 'member')

        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user