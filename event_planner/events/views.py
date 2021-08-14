from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from event_planner.events.forms import CreateEventForm, UpdateEventForm
from event_planner.events.models import Event
from datetime import datetime
from django.utils import timezone


def home(request):
    # events = Event.objects.all()
    past_events = Event.objects.filter(start_datetime__lt=timezone.now())
    future_events = Event.objects.filter(start_datetime__gte=timezone.now())
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


class EventDetails(DetailView):
    model = Event
    template_name = 'events/event_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guests'] = self.object.guests.all()
        # event = get_object_or_404(Event, id=self.kwargs['pk'])
        joined = False
        if self.object.guests.filter(id=self.request.user.id).exists():
            joined = True
        context['number_of_guests'] = self.object.number_of_guests()
        context['joined_event'] = joined
        return context


class UpdateEvent(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = UpdateEventForm
    template_name = 'events/update_event.html'

    def test_func(self):
        return self.request.user == self.get_object().creator

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.start_datetime < timezone.now():
            raise PermissionDenied
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.start_datetime < timezone.now():
            raise PermissionDenied
        return super().get(request, *args, **kwargs)


class DeleteEvent(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user == self.get_object().creator


@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, id=request.POST.get('event_id'))
    if event.start_datetime < timezone.now():
        raise PermissionDenied
    if event.guests.filter(id=request.user.id).exists():
        event.guests.remove(request.user)
    else:
        event.guests.add(request.user)

    # return HttpResponseRedirect(reverse('blogpost-detail', args=[str(pk)]))
    return redirect('event details', pk=pk)
