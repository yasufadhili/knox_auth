from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db import models

from rest_framework import viewsets, permissions, status, generics, serializers
from rest_framework.fields import empty
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from knox.models import AuthToken

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
        fields = ["id", "username", "phone_number", "first_name", "last_name", "email", "is_developer", "is_moderator", "date_joined", "last_login", "profile"]
        #fields = "__all__"


class UserRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRelationship
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "email", "first_name", "last_name", "password")
        extra_kwargs = {
            "password": {
                "write_only": True,
              "style": {"input_type": "password"}
            }
        }
    
    def validate_phone_number(self, phone_number):
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Phone number '%s' already exists")
        return phone_number
    
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username '%s already exists" % username)
        return username

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            phone_number=validated_data["phone_number"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class UserLoginSerializer(AuthTokenSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "password")
    

class UserRelationshipSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    class Meta:
        model = UserRelationship
        fields = ('follower', 'following')
    def create(self, validated_data):
        follower = self.context['request'].user
        following = validated_data['following']
        relationship = UserRelationship.objects.create(follower=follower, following=following)
        return relationship



class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('country', 'bio', 'display_image')
    
    def update(self, instance, validated_data):
        instance.country = validated_data['country']
        instance.bio = validated_data['bio']
        instance.display_image = validated_data['display_image']
        instance.save()
        return instance



