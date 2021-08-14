from django.urls import path

from event_planner.accounts.views import SignInView, sign_up, ProfileDetails, UpdateProfile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='sign in'),
    path('signout/', LogoutView.as_view(next_page='sign in'), name='sign out'),
    path('signup/', sign_up, name='sign up'),
    path('profile/<int:pk>', ProfileDetails.as_view(), name='profile details'),
    path('update/<int:pk>', UpdateProfile.as_view(), name='update profile'),
]