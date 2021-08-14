from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from event_planner.accounts.models import UserProfile
from event_planner.events.forms import BootstrapFormMixin

UserModel = get_user_model()


class SignInForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)


class UpdateProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
