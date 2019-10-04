from django.db import models
from django.db.models import Count, Q
from django.utils.text import slugify


class Blog(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=50000)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='blog', on_delete=models.CASCADE, null=True)
    image = models.FileField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True, default='', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

    @property
    def votes(self):
        return Blog.objects.aggregate(
            total_votes=(
                    Count('post_votes', filter=Q(post_votes__vote_type='U') & Q(post_votes__blog=self)) -
                    Count('post_votes', filter=Q(post_votes__vote_type='D') & Q(post_votes__blog=self))
            )
        )

    def upvote(self, user):
        vote, created = self.post_votes.get_or_create(user=user, blog=self)
        if not created and vote.vote_type == 'U':
            return 'You have already up voted this blog post.'

        vote.vote_type = 'U'
        vote.save()
        return 'You have successfully up voted this blog post.'

    def downvote(self, user):
        vote, created = self.post_votes.get_or_create(user=user, blog=self)
        if not created and vote.vote_type == 'D':
            return 'You have already down voted this blog post.'

        vote.vote_type = 'D'
        vote.save()
        return 'You have successfully down voted this blog post.'


class Comment(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='reply', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='comment', on_delete=models.CASCADE)
    description = models.TextField(max_length=50000)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='comment', on_delete=models.CASCADE, null=True)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class UserVote(models.Model):
    VOTE_CHOICES = (
        ('U', 'Upvote'),
        ('D', 'Downvote'),
    )
    user = models.ForeignKey('auth.User', related_name='user_votes', on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name='post_votes', on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=1, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'blog')
