from django.urls import path

from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserRegistrationView, UserLoginView, UserView


router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-registration"),
    path("login/", UserLoginView.as_view(), name="user-login"),

    path("<str:username>/", UserView.as_view(), name="user-view"),
]

urlpatterns += router.urls



