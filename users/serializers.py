from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Profile, ProfileStatus, UserRelationship


User = get_user_model()


class ProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileStatus
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    profile_status = ProfileStatusSerializer(read_only=False)
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=False)
    class Meta:
        model = User
        fields = '__all__'


class UserRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelationship
        fields = '__all__'

