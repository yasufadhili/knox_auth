from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.db import models

from rest_framework import viewsets, permissions, generics, views, response, status, serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from users.serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer, ProfileSerializer, UserRelationshipSerializer, UserRelationship


User = get_user_model()


from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAdminUser]


class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(KnoxLoginView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = User.objects.filter(
            models.Q(username=username)
        ).first()
        if user:
            if not user.check_password(password):
                message = "Incorrect Password..."
                raise serializers.ValidationError(message, code="authorization")
        else:
            message = "Unable to authenticate with provided credentials."
            raise serializers.ValidationError(message, code="authorization")
        token, _ = AuthToken.objects.create(user=user)
        attrs["user"] = user
        attrs["token"] = token
        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "phone_number": user.phone_number,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "token": token.key
        }
        return response_data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        token, _ = AuthToken.objects.create(user=user)
        response_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "phone_number": user.phone_number,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
        }
        return response.Response(response_data)



class UserProfileView(generics.ListAPIView):
    """
    API Endpoint to view user profiles for a given user
    """
    serializer_class = ProfileSerializer
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        profile = user.profile
        serializer = ProfileSerializer(profile)
        return response.Response(serializer.data)


class UserFollowersView(generics.ListAPIView):
    """
    API Endpoint to view users' followers
    """
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRelationshipSerializer
    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, id=user_id)
        return UserRelationship.objects.filter(following=user)


class UserFollowingView(generics.ListAPIView):
    """
    API Endpoint for viewing users' following
    """
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserRelationshipSerializer
    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        user = get_object_or_404(User, id=user_id)
        return UserRelationship.objects.filter(follower=user)


class UserRelationshipCreateView(generics.CreateAPIView):
    """
    API Endpoint for creating a user relationship
    """
    serializer_class = UserRelationshipSerializer
    def post(self, request, *args, **kwargs):
        following_id = request.data.get("following_id")
        follower = request.user
        if UserRelationship.objects.filter(follower=follower, follower_id=following_id).exists():
            return response.Response({"message": "You are already following this user"})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exceptions=True)
        serializer.save()
        return response.Response(serializer.data, status=status.status.HTTP_201_CREATED)


class UserRelationshipDeleteView(generics.DestroyAPIView):
    """
    API Endpoint for deleting a user relationship
    """
    queryset = UserRelationship.objects.all()
    serializer_class = UserRelationshipSerializer
    lookup_field = "following_id"

    def delete(self, request, *args, **kwargs):
        follower = request.user
        following_id = kwargs.get("following_id")

        # Check if the user is following the target user
        try:
            relationship = UserRelationship.objects.get(follower=follower, following_id=following_id)
        except UserRelationship.DoesNotExist:
            return response.Response({"message": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(relationship)
        return response.Response(status=status.HTTP_204_NO_CONTENT)




