
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'phone_number')


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'phone_number')