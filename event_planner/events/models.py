from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, date

# Create your models here.
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    info = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    start_datetime = models.DateTimeField()
    guests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='guest_at_events')

    def number_of_guests(self):
        return self.guests.count()

    def __str__(self):
        return f"{self.title} | {self.creator}"

    @staticmethod
    def get_absolute_url():
        return reverse('home')

