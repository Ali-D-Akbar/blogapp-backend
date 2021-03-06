import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from accounts.views import RegisterAPI
from blog.models import Blog
from blog.views import BlogAPI

pytestmark = pytest.mark.django_db


class BlogTests(APITestCase):
    """
    Tests for Blog.
    """
    def register(self, credentials):
        """
        Registers a user given the credentials for test purposes.
        """
        factory = APIRequestFactory()
        view = RegisterAPI.as_view()
        url = '/api/auth/register'

        request = factory.post(url, credentials)
        return view(request)

    def create_blog_request(self, body):
        """
        Creates a Blog Post.
        """
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }

        self.register(credentials)

        factory = APIRequestFactory()
        url = '/api/blog'

        request = factory.post(url, body)
        return request

    def test_get_blog_list_authorized(self):
        """
        Tests to get a list of Blog Post, authorized.
        """
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }

        response = self.register(credentials)

        factory = APIRequestFactory()
        view = BlogAPI.as_view({
            'get': 'list'
        })
        url = '/api/blog'
        user = User.objects.get(username='test')

        request = factory.get(url)
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_blog(self):
        """
        Tests to create a Blog Post Successfully.
        """
        body = {
            'title': 'Test',
            'description': 'This is a Test Blog.'
        }
        request = self.create_blog_request(body)
        user = User.objects.get(username='test')
        view = BlogAPI.as_view({
            'post': 'create'
        })

        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().title, 'Test')

    def test_create_blog_failed(self):
        """
        Tests to create a Blog Post Unsuccessfully.
        """
        body = {
            'title': 'This is a Test Blog.'
        }
        view = BlogAPI.as_view({
            'post': 'create'
        })
        request = self.create_blog_request(body)
        user = User.objects.get(username='test')

        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_blog(self):
        """
        Tests to delete a Blog Post.
        """
        body = {
            'title': 'Test',
            'description': 'This is a Test Blog to be deleted.'
        }
        request = self.create_blog_request(body)
        user = User.objects.get(username='test')
        view = BlogAPI.as_view({
            'post': 'create'
        })

        force_authenticate(request, user=user)
        response = view(request)

        blog = Blog.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 1)
        self.assertEqual(Blog.objects.get().title, 'Test')

        view = BlogAPI.as_view({
            'delete': 'destroy'
        })
        url = '/api/blog'
        factory = APIRequestFactory()
        request = factory.delete(url)

        force_authenticate(request, user=user)
        response = view(request, slug=blog.slug)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
