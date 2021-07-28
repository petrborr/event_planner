from django.urls import path

from event_planner.accounts.views import SignInView, sign_up
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='sign in'),
    path('signout/', LogoutView.as_view(next_page='sign in'), name='sign out'),
    path('signup/', sign_up, name='sign up'),
]