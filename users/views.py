from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets, permissions, generics

from users.serializers import UserSerializer, UserRegistrationSerializer


User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


