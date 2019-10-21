from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from blog.models import Blog, Comment, Profile, UserVote


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'  # Foreign Key Name


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_select_related = ('profile',)
    list_display = (
        'username', 'first_name', 'last_name', 'get_date_of_birth', 'email',
        'get_gender', 'get_contact_number', 'get_country'
    )

    def get_date_of_birth(self, instance):
        return instance.profile.date_of_birth

    get_date_of_birth.short_Description = 'Date of Birth'

    def get_gender(self, instance):
        return instance.profile.gender

    get_gender.short_description = 'Gender'

    def get_contact_number(self, instance):
        return instance.profile.contact_number

    get_contact_number.short_description = 'Contact Number'

    def get_country(self, instance):
        return instance.profile.country

    get_country.short_description = 'Country'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(UserVote)
