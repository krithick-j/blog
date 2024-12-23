from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    # Custom fields for your User model
    is_owner = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    # Overriding the groups field to prevent reverse relation conflict
    groups = models.ManyToManyField(
        Group, 
        related_name='api_user_set',  # Custom related name to avoid clash
        blank=True
    )

    # Overriding the user_permissions field to prevent reverse relation conflict
    user_permissions = models.ManyToManyField(
        Permission, 
        related_name='api_user_permissions',  # Custom related name to avoid clash
        blank=True
    )

class Article(models.Model):
    # Fields for Article model
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # Fields for Comment model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
