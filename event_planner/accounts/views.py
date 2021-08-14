from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView

from event_planner.accounts.forms import SignInForm, SignUpForm, UpdateProfileForm
from event_planner.accounts.models import CustomUser, UserProfile


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


class ProfileDetails(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/profile_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guest_at'] = self.get_object().user.guest_at_events.all()
        return context


class UpdateProfile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    form_class = UpdateProfileForm
    template_name = 'accounts/update_profile.html'

    def get_success_url(self):
        return reverse_lazy('profile details', kwargs={'pk': self.request.user.id})

    def test_func(self):
        return self.request.user.id == self.get_object().user.pk
