from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.models import Blog, Comment, Profile, UserVote
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import BlogSerializer, CommentSerializer, ProfileSerializer, UserSerializer, VoteSerializer


class BlogAPI(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions for Blog Model.
    """
    queryset = Blog.objects.all()

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,
    ]

    lookup_field = 'slug'

    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        """
        Custom create method for Blog Post.
        Saves Currently logged in user with the post.
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Custom Update method for Blog Post.
        """
        serializer.save(created=timezone.now())

    def list(self, request, *args, **kwargs):
        """
        Custom List method for Blog Post.
        Can filter List based on search criteria.
        """
        if request.GET.get('keyword', '') != '':
            queryset = Blog.objects.filter(
                Q(title__icontains=request.GET.get('keyword')) | Q(description__contains=request.GET.get('keyword'))
            )

        elif request.user.is_authenticated:
            queryset = Blog.objects.filter(
                Q(draft=False) | (Q(draft=True) & Q(owner=request.user))
            )

        else:
            queryset = Blog.objects.filter(
                Q(draft=False)
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BlogSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = BlogSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True)
    def upvote(self, request, *args, **kwargs):
        """
        Fires Upvote Action
        """
        blog = self.get_object()
        return Response(blog.upvote(request.user))

    @action(detail=True)
    def downvote(self, request, *args, **kwargs):
        """
        Fires Downvote Action
        """
        blog = self.get_object()
        return Response(blog.downvote(request.user))


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions for User Model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class CommentAPI(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions for Comment Model.
    """
    queryset = Comment.objects.all()

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        """
        Saves the comment of the currently logged user.
        """
        serializer.save(owner=self.request.user)


class VoteAPI(viewsets.ModelViewSet):
    queryset = UserVote.objects.all()
    serializer_class = VoteSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions for Profile Model
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
