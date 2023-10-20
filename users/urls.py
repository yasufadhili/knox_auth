from django.urls import path

from rest_framework.routers import DefaultRouter

from users import views


router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="user-registration"),
    path("login/", views.UserLoginView.as_view(), name="user-login"),

    #path("<str:username>/", views.UserView.as_view(), name="user-view"),

    path('<str:id>/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('<str:user_id>/followers/', views.UserFollowersView.as_view(), name='user_followers'),
    path('<str:user_id>/following/', views.UserFollowingView.as_view(), name='user_following'),

    path('relationship/create/', views.UserRelationshipCreateView.as_view(), name='user_relationship-create'),
    path('relationship/delete/<str:following_id>/', views.UserRelationshipDeleteView.as_view(), name='user-relationship-delete'),

]

urlpatterns += router.urls



