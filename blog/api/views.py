from django.http import JsonResponse
from rest_framework import viewsets
from .models import Article, Comment, FeatureFlag, User
from .serializers import ArticleSerializer, CommentSerializer, FeatureFlagSerializer, UserSerializer
from .permissions import IsAdmin, IsMember
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from dotenv import load_dotenv 
import os
 
# Load environment variables from the .env file
load_dotenv()

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

    # @feature_flag_enabled("manage_article_permissions") #feature flag work in progress
    def perform_create(self, serializer):
        print(f"Feature flag 'manage_article_permissions' is enabled.")  # Debugging line

        # Automatically set the authenticated user as the author
        serializer.save(author=self.request.user)

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

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from api.models import Article, FeatureFlag, Tag
import openai

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMArticleViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling Articles with feature flags for LLM-based content and tag generation.
    """
    # Set the permission to ensure the user is authenticated
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List all articles.
        """
        articles = Article.objects.all()
        data = [{"id": article.id, "title": article.title, "content": article.content, "tags": [tag.name for tag in article.tags.all()]} for article in articles]
        return Response(data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a single article by its ID.
        """
        try:
            article = Article.objects.get(pk=pk)
            data = {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "tags": [tag.name for tag in article.tags.all()],
            }
            return Response(data)
        except Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        Create a new article. If LLM Article Generation is enabled, generate content if not provided.
        If LLM Tags Generation is enabled, generate tags for the article.
        """
        title = request.data.get("title", "")
        content = request.data.get("content", "")
        tags = request.data.get("tags", [])

        if not title:
            return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get feature flags
        feature_flags = self._get_feature_flags()

        # Generate content if LLM Article Generation is enabled and content is empty
        if not content and feature_flags.get("LLM Article Generation", False):
            content = self.generate_llm_content(title)

        # Get the authenticated user (author) from the token
        author = request.user  # This assumes you are using token-based authentication and the user is authenticated

        # Create the article
        article = Article.objects.create(
            title=title, 
            content=content,
            author=author  # Ensure that the author is set to the authenticated user
        )

        # Generate tags if LLM Tags Generation is enabled
        if feature_flags.get("LLM Tags Generation", False):
            suggested_tags = self.generate_llm_tags(content)
            for tag_name in suggested_tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                article.tags.add(tag)

        article.save()

        return Response({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "tags": [tag.name for tag in article.tags.all()],
        }, status=status.HTTP_201_CREATED)

    def _get_feature_flags(self):
        """
        Retrieve feature flags from the cache or database.
        """
        cache_key = "feature_flags"
        flags = cache.get(cache_key)
        if flags is None:
            flags = {flag.name: flag.is_active for flag in FeatureFlag.objects.all()}
            cache.set(cache_key, flags, timeout=3600)  # Cache for 1 hour
        return flags

    def generate_llm_content(self, title):
        """
        Generate article content using OpenAI's GPT model (e.g., gpt-3.5-turbo).
        """
        try:
            # Prepare the messages for the new API format
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Write a detailed blog article about: {title}"}
            ]
            
            # Call the OpenAI API with the correct parameters
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # You can also use "gpt-4" if you prefer
                messages=messages,
                max_tokens=500,  # You can adjust this value based on your needs
            )
            # Return the generated content from the assistant's reply
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Failed to generate content: {str(e)}"

    def generate_llm_tags(self, content):
        """
        Generate tags for the article content using OpenAI.
        """
        try:
            # Prepare the messages for tag generation
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Suggest 5 relevant tags with comma seperated for the following article content:\n\n{content}"}
            ]
            
            # Call the OpenAI API to generate tags
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # You can also use "gpt-4" here if preferred
                messages=messages,
                max_tokens=50,  # You can adjust this value based on the length of the tags
            )
            # Extract the tags from the assistant's response
            tags = response.choices[0].message.content.split(", ")
            return tags
        
        except Exception as e:
            return [f"Error: {str(e)}"]
