
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from django_countries.fields import CountryField

from users.managers import UserManager

import shortuuid


class User(AbstractUser):
    id = models.CharField(_(u'id'),
                          primary_key=True,
                          max_length=255,
                          default=shortuuid.uuid,
                          help_text=u'User ID',
                          db_index=True)
    username = models.CharField(max_length=255,
                                validators=[
                                    RegexValidator(
                                        regex="^[0-9a-zA-Z]*$", message="Username can only contain alphanumeric characters i.e 0-9 a-z A-Z."
                                    )
                                ],
                                unique=True, )
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(_("Phone Number"),max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    user_relationships = models.ManyToManyField("self",
                                                through="UserRelationship",
                                                symmetrical=False,
                                                related_name="related_to")
    is_developer = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number",]

    def __str__(self):
        return self.username


class UserRelationship(models.Model):
    follower = models.ForeignKey(get_user_model(),
                                 related_name="following" ,
                                 on_delete=models.CASCADE)
    following = models.ForeignKey(get_user_model(),
                                 related_name="followers",
                                 on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

# Create a follow relationship
'''
follower = User.objects.get(username='follower_username')
following = User.objects.get(username='following_username')
relationship = UserRelationship.objects.create(follower=follower, following=following)
'''
# Get followers and following of a user
'''user = User.objects.get(username='username')
followers = user.followers.all()
following = user.following.all()'''

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=1000)
    display_image = models.URLField(blank=True, null=True)
    status = models.ForeignKey("ProfileStatus", blank=True, null=True, on_delete=models.CASCADE, related_name="profile_status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def followers_count(self):
        return self.user.followers.count()
    
    def following_count(self):
        return self.user.following.count()
    
    def profile_status(self):
        try:
            profile_status = ProfileStatus.objects.get(profile=self)
            return profile_status.status
        except ProfileStatus.DoesNotExist:
            return "No status set"

    def __str__(self):
        return self.user.username


class ProfileStatus(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(choices=(
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('banned', 'Banned'),
    ), default='active', max_length=100, blank=True)
    reason = models.TextField(blank=True, null=True, max_length=1000)
    reconsidered_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile Status")
        verbose_name_plural = _("Profile Statuses")

    def __str__(self):
        return self.status

