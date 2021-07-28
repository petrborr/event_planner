from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, UpdateView, DetailView

from event_planner.events.forms import CreateEventForm, UpdateEventForm, DeleteEventForm
from event_planner.events.models import Event
from datetime import datetime


def home(request):
    # events = Event.objects.all()
    past_events = Event.objects.filter(start_datetime__lt=datetime.today())
    future_events = Event.objects.filter(start_datetime__gt=datetime.today())
    context = {
        'events': future_events,
        'past_events': past_events
    }
    return render(request, 'events/home.html', context)


class CreateEvent(CreateView):
    model = Event
    form_class = CreateEventForm
    template_name = 'events/create_event.html'


class EventDetail(DetailView):
    model = Event


class UpdateEvent(UpdateView):
    model = Event
    form_class = UpdateEventForm
    template_name = 'events/update_event.html'


class DeleteEvent(UpdateView):
    model = Event
    form_class = DeleteEventForm
    template_name = 'events/delete_event.html'
