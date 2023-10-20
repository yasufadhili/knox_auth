from django.contrib.auth import get_user_model

from rest_framework import serializers

from django_countries.serializers import CountryFieldMixin

from users.models import Profile, ProfileStatus, UserRelationship


User = get_user_model()


class ProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileStatus
        fields = ["status",]


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    status = ProfileStatusSerializer(read_only=False)
    class Meta:
        model = Profile
        fields = ["country", "bio", "display_image", "status", "followers_count", "following_count"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=False)
    class Meta:
        model = User
        fields = ["id", "username", "phone_number", "last_name", "first_name", "email", "is_developer", "is_moderator", "date_joined", "last_login", "profile"]
        #fields = "__all__"


class UserRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelationship
        fields = '__all__'

