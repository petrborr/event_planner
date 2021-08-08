from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import View
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


class CreateEvent(LoginRequiredMixin, CreateView):
    model = Event
    form_class = CreateEventForm
    template_name = 'events/create_event.html'

    def form_valid(self, form):
        event = form.save(commit=False)
        event.creator = self.request.user
        event.save()
        return redirect('home')


#
class EventDetails(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guests'] = self.object.guests.all()

        likes_connected = get_object_or_404(Event, id=self.kwargs['pk'])
        joined = False
        if likes_connected.guests.filter(id=self.request.user.id).exists():
            joined = True
        context['number_of_guests'] = likes_connected.number_of_guests()
        context['joined_event'] = joined
        return context


class UpdateEvent(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = UpdateEventForm
    template_name = 'events/update_event.html'

    def test_func(self):
        return self.request.user == self.get_object().creator


class DeleteEvent(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = DeleteEventForm
    template_name = 'events/delete_event.html'


@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, id=request.POST.get('event_id'))
    if event.guests.filter(id=request.user.id).exists():
        event.guests.remove(request.user)
    else:
        event.guests.add(request.user)

    # return HttpResponseRedirect(reverse('blogpost-detail', args=[str(pk)]))
    return redirect('event details', pk=pk)
