from django.forms import ModelForm
from django.forms.widgets import EmailInput
from django.db import models
from django import forms
from .models import Event , TicketPurchase


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date' , 'time' ,  'type' , 'public' ,  'price', 'available_tickets' , 'description' ,  'image' ]
        name = forms.CharField(max_length=100)
        image = forms.ImageField(required=False)
        price = forms.DecimalField(max_digits=10, decimal_places=2, min_value=3, required=False )

        widgets = {
            'description': forms.Textarea(),
            'date': DateInput(),
            'time': TimeInput()
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'input'




class TicketPurchaseForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super().__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs.update({'max': self.event.available_tickets})

class ContactUsForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)



