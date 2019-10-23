from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from blog.models import Blog, Comment, Profile, UserVote


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the profile of a user.
    """
    userid = serializers.ReadOnlyField(source='user.username')

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = Profile
        fields = (
            'url', 'id', 'userid', 'gender', 'contact_number', 'date_of_birth',
            'image', 'country'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the Custom User Model.
    """
    blog = serializers.ReadOnlyField(source='blog.title')
    profile = ProfileSerializer(read_only=True)

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = User
        fields = [
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'blog', 'profile'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class ReplySerializer(serializers.ModelSerializer):
    """
    Serializes data of Replies of Comments.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = Comment
        fields = ['parent', 'id', 'description', 'created', 'owner']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializes the data of a comment.
    """
    owner = UserSerializer(read_only=True)
    blog = serializers.HyperlinkedRelatedField(
        view_name='blog-detail',
        lookup_field='slug',
        queryset=Blog.objects.all()
    )
    reply = SerializerMethodField()

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = Comment
        fields = [
            'parent', 'id', 'blog', 'description', 'created', 'owner', 'reply'
        ]

    def get_reply(self, obj):
        """
        Serializer Method to get reply field.
        """
        if obj.is_parent:
            return ReplySerializer(
                obj.children(), many=True,
                context={'request': self.context['request']}
            ).data

        return None


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the data of Blog Posts.
    """
    owner = UserSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = Blog
        fields = [
            'url', 'slug', 'id', 'title', 'description', 'created', 'owner',
            'image', 'votes', 'comment', 'draft'
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes the data of Votes on Blog Posts.
    """
    user = serializers.ReadOnlyField(source='user.username')
    blog = serializers.HyperlinkedRelatedField(
        view_name='blog-detail', lookup_field='slug',
        queryset=Blog.objects.all()
    )

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = UserVote
        fields = ['url', 'id', 'user', 'blog', 'vote_type']
