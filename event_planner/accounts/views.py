from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from event_planner.accounts.forms import SignInForm, SignUpForm
from event_planner.accounts.models import CustomUser


class SignInView(LoginView):
    model = CustomUser
    form_class = SignInForm
    template_name = 'accounts/signin.html'
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse_lazy('home')


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        if request.user.is_authenticated:
            return redirect('home')
        form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/signup.html', context)


class UpdateProfile(UpdateView):
    pass
