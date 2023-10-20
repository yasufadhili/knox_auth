from django.urls import path

from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserRegistrationView, UserLoginView


router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),
]

urlpatterns += router.urls



