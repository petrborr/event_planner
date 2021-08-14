from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from event_planner.accounts.models import CustomUser
from event_planner.events.models import Event


class HomeViewTest(TestCase):
    def test_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/home.html')


class CreateEventViewTest(TestCase):
    def test_view_with_user_returns_form(self):
        test_user = CustomUser.objects.create_user(email='account1@gmail.com', password='user_password123')
        test_user.save()
        self.client.force_login(test_user)
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create_event.html')

    def test_view_url_accessible_by_name(self):
        test_user = CustomUser.objects.create_user(email='account1@gmail.com', password='user_password123')
        test_user.save()
        self.client.force_login(test_user)
        response = self.client.get(reverse('create event'))
        self.assertEqual(response.status_code, 200)

    def test_view_without_user_returns_302(self):
        response = self.client.get(reverse('create event'))
        self.assertEqual(response.status_code, 302)

    def test_view_with_user_can_create_event(self):
        test_user = CustomUser.objects.create_user(email='account1@gmail.com', password='user_password123')
        test_user.save()
        self.client.force_login(test_user)
        self.client.post('/create/', {
            'creator': 'account1@gmail.com',
            'title': 'event_title_test',
            'info': 'whatever',
            'start_datetime': '2022-10-25 14:30:59'
        })
        self.assertEqual(Event.objects.last().title, 'event_title_test')
