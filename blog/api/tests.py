from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from blog import settings

class ArticleRBACPermissionTest(TestCase):
    def setUp(self):
        User = get_user_model()  # Get the custom User model
  # Get the custom User model
        # Create test users with different roles
        self.client = APIClient()

        # In setUp, after creating adminUser
        self.admin_user = User.objects.create_superuser(username='adminUser', password='123456')
        self.admin_user.role = "admin"
        self.admin_user.save()

        # Create a token for the admin user
        self.admin_user_token = Token.objects.create(user=self.admin_user)


        self.member_user = User.objects.create_user(
            username='memberUser', password='123456'
        )
        self.member_user.role = "member"
        self.member_user.save()

        self.article_url = '/api/articles/'  # Replace with your actual article creation endpoint

    def get_jwt_token(self, username, password):
        """Helper function to obtain JWT token."""
        response = self.client.post('/api/token/', {'username': username, 'password': password})
        return response.data['access']  # Extract the 'access' token

    def test_admin_can_create_article(self):
        """Test admin user can create an article."""
        loggedin = self.client.login(username='adminUser', password='123456')
        # Check if login was successful
        self.assertTrue(loggedin, "Admin user failed to log in")
        token = self.get_jwt_token('adminUser', '123456')
        # Make the POST request with the authorization header
        response = self.client.post(path=self.article_url, 
                                    data={'title': 'Test Article', 'content': 'Test Content'}, 
                                    headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_cannot_create_article(self):
        """Test admin user can create an article."""
        loggedin = self.client.login(username='memberUser', password='123456')
        # Check if login was successful
        self.assertTrue(loggedin, "Admin user failed to log in")
        token = self.get_jwt_token('memberUser', '123456')
        # Make the POST request with the authorization header
        response = self.client.post(path=self.article_url, 
                                    data={'title': 'Test Article', 'content': 'Test Content'}, 
                                    headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_create_article(self):
        """Test unauthenticated user cannot create an article."""
        response = self.client.post(self.article_url, {'title': 'Test Article', 'content': 'Test Content'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
