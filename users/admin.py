from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Profile, ProfileStatus

User = get_user_model()


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_developer', 'is_moderator', 'is_active')
    list_filter = ('is_developer', 'is_moderator')
    search_fields = ('username', 'email', 'phone_number')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('is_developer', 'is_moderator')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone_number', 'is_developer', 'is_moderator'),
        }),
    )

admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'followers_count', 'following_count', 'get_status',)
    search_fields = ('user__username', 'country', 'profilestatus__status')
    list_filter = ('profilestatus__status','country',)

    def followers_count(self, obj):
        return obj.followers_count()

    def following_count(self, obj):
        return obj.following_count()
    
    def get_status(self, obj):
        try:
            profile_status = ProfileStatus.objects.get(profile=obj)
            return profile_status.status
        except ProfileStatus.DoesNotExist:
            return "No status available"

    followers_count.short_description = 'Followers'
    following_count.short_description = 'Following'
    get_status.short_description = 'Status'


admin.site.register(Profile, ProfileAdmin)

class ProfileStatusAdmin(admin.ModelAdmin):
    list_display = ("profile", "status", "reconsidered_at",)
    list_filter = ("status", "reconsidered_at",)

admin.site.register(ProfileStatus, ProfileStatusAdmin)
