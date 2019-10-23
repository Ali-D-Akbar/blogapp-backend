from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django_countries.fields import CountryField


class Blog(models.Model):
    """
    Model to save data of Blog Posts.
    """
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=50000)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='blog', on_delete=models.CASCADE, null=True)
    image = models.FileField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True, default='', blank=True)

    def save(self, *args, **kwargs):
        """
        Additionally saves the slug field.
        """
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        """
        Meta class for ordering.
        """
        ordering = ['-created']

    @property
    def votes(self):
        """
        Calculates difference between Upvotes and Downvotes.
        """
        return Blog.objects.aggregate(
            total_votes=Count(
                'post_votes', filter=(Q(post_votes__vote_type='U') & Q(post_votes__blog=self))
            ) - Count(
                'post_votes', filter=(Q(post_votes__vote_type='D') & Q(post_votes__blog=self))
            )
        )

    def upvote(self, user):
        """
        Performs Upvote.
        """
        vote, created = self.post_votes.get_or_create(user=user, blog=self)
        if not created and vote.vote_type == 'U':
            return 'You have already up voted this blog post.'

        vote.vote_type = 'U'
        vote.save()
        return 'You have successfully up voted this blog post.'

    def downvote(self, user):
        """
        Performs Downvote
        """
        vote, created = self.post_votes.get_or_create(user=user, blog=self)
        if not created and vote.vote_type == 'D':
            return 'You have already down voted this blog post.'

        vote.vote_type = 'D'
        vote.save()
        return 'You have successfully down voted this blog post.'


class Comment(models.Model):
    """
    Model to save data of Comments on Blog Posts.
    """
    parent = models.ForeignKey('self', blank=True, null=True, related_name='reply', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='comment', on_delete=models.CASCADE)
    description = models.TextField(max_length=50000)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        'auth.User', related_name='comment',
        on_delete=models.CASCADE, null=True
    )

    def children(self):
        """
        Returns the children of a comment.
        """
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        """
        Determines if a Comment is a Parent Comment.
        """
        if self.parent is not None:
            return False
        return True


class UserVote(models.Model):
    """
    Model to save data of Votes on Blog Posts.
    """
    VOTE_CHOICES = (
        ('U', 'Upvote'),
        ('D', 'Downvote'),
    )
    user = models.ForeignKey('auth.User', related_name='user_votes', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='post_votes', on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=1, choices=VOTE_CHOICES)

    class Meta:
        """
        Meta class for unique_together relationship.
        """
        unique_together = ('user', 'blog')


class Profile(models.Model):
    """
    Custom User Model.
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    contact_number = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.FileField(blank=True, null=True)
    country = CountryField(default="US")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """
        Creates a Profile associated with a User.
        """
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """
        Saves Profile data associated with a User.
        """
        instance.profile.save()
