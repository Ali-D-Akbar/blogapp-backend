# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from accounts.views import RegisterAPI
from blog.models import Blog
from blog.views import BlogAPI


class BlogTests(APITestCase):
    def register(self, credentials):
        factory = APIRequestFactory()
        view = RegisterAPI.as_view()
        url = '/api/auth/register'

        request = factory.post(url, credentials)
        return view(request)

    def create_blog_request(self, body):
        credentials = {
            'username': 'test',
            'email': 'abc@example.com',
            'password': '123'
        }

        response = self.register(credentials)

        factory = APIRequestFactory()
        url = '/api/blog'

        request = factory.post(url, body)
        return request

    def test_get_blog_list_unauthorized(self):
        factory = APIRequestFactory()
        view = BlogAPI.as_view({
            'get': 'list'
        })
        url = '/api/blog'

        request = factory.get(url)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_blog_list_authorized(self):
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
        response = view(request, pk=blog.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
