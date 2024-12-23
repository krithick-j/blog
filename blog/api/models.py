from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model

ROLE_CHOICES = (
    ('owner', 'Owner'),
    ('admin', 'Admin'),
    ('member', 'Member'),
)

class User(AbstractUser):
    # Custom fields for your User model
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='member',  # Default role is member
    )

    # Overriding the groups field to prevent reverse relation conflict
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='api_user_set',  # Custom related name to avoid clash
        blank=True
    )

    # Overriding the user_permissions field to prevent reverse relation conflict
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='api_user_permissions',  # Custom related name to avoid clash
        blank=True
    )
# Get the User model (default is auth.User)
User = get_user_model()

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255)  # For simplicity, assuming tags as comma-separated string
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model (author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.article.title}"

