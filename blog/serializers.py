from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from blog.models import Blog, Comment, Profile, UserVote


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    userid = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = (
            'url', 'id', 'userid', 'gender', 'contact_number', 'date_of_birth',
            'image', 'country'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    blog = serializers.ReadOnlyField(source='blog.title')
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'url', 'id', 'username', 'first_name', 'last_name', 'email',
            'blog', 'profile'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class ReplySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['parent', 'id', 'description', 'created', 'owner']


class CommentSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    blog = serializers.HyperlinkedRelatedField(
        view_name='blog-detail',
        lookup_field='slug',
        queryset=Blog.objects.all()
    )
    reply = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'parent', 'id', 'blog', 'description', 'created', 'owner', 'reply'
        ]

    def get_reply(self, obj):
        if obj.is_parent:
            return ReplySerializer(
                obj.children(), many=True,
                context={'request': self.context['request']}
            ).data

        return None


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = [
            'url', 'slug', 'id', 'title', 'description', 'created', 'owner',
            'image', 'votes', 'comment', 'draft'
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class VoteSerializer (serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    blog = serializers.HyperlinkedRelatedField(
        view_name='blog-detail', lookup_field='slug',
        queryset=Blog.objects.all()
    )

    class Meta:
        model = UserVote
        fields = ['url', 'id', 'user', 'blog', 'vote_type']
