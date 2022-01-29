from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import  UserMaster


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserMaster
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = UserMaster
        fields = ('email',)