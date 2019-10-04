from django.contrib import admin

from blog.models import Blog, Comment, UserVote

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(UserVote)
