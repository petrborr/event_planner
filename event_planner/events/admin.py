from django.contrib import admin

# Register your models here.
from event_planner.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
