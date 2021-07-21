from django import forms

from event_planner.events.models import Event


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_fields()

    def _init_bootstrap_fields(self):
        for (_, field) in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form-control'


class CreateEventForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        # widgets = {
        #     'start_datetime': forms.DateTimeInput(attrs={'type': 'date'})
        # }


class UpdateEventForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


class DeleteEventForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['disabled'] = 'disabled'
            visible.field.widget.attrs['required'] = 'required'

    class Meta:
        model = Event
        fields = '__all__'
