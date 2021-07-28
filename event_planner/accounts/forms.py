from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

UserModel = get_user_model()


class SignInForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)
