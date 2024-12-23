from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model

from blog import settings

ROLE_CHOICES = (
    ('owner', 'Owner'),
    ('admin', 'Admin'),
    ('member', 'Member'),
    ('super_admin', 'Super Admin'),  # Added super_admin
)
class User(AbstractUser):
    # Custom fields for your User model
    role = models.CharField(
        max_length=30, 
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
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to the custom User model
        on_delete=models.CASCADE,
        related_name="articles"  # For reverse relationship
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"  # For reverse relationship
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to the custom User model
        on_delete=models.CASCADE,
        related_name="comments"  # For reverse relationship
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"

class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    actions = models.JSONField(default=dict)  # Store allowed actions for the flag


    def __str__(self):
        return self.name
    
    def get_actions(self):
        return self.actions if self.actions else {}

    def is_action_enabled(self, action):
        actions = self.get_actions()
        return actions.get(action, False)  # Return True or False based on action