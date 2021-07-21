from django.urls import path

from event_planner.events.views import home, CreateEvent, UpdateEvent, DeleteEvent

urlpatterns = [
    path('', home, name='home'),
    path('create/', CreateEvent.as_view(), name='create event'),
    path('update/<int:pk>', UpdateEvent.as_view(), name='update event'),
    path('delete/<int:pk>', DeleteEvent.as_view(), name='delete event'),
]