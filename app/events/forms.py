from django import forms
from django.forms import ModelForm
from. models import Venue, Event
#admin superuser form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ( 'name', 'event_date', 'venue', 'manager', 'attendees', 'description')
        labels ={
             'name': '',
            'event_date': 'YYYY-MM-DD  HH:MM:SS',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
            
        }  
        widgets={


            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event date'}),
            'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
            'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'manager'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Poeple'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),

        }   



#user event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ( 'name', 'event_date', 'venue', 'attendees', 'description')
        labels ={
             'name': '',
            'event_date': 'YYYY-MM-DD  HH:MM:SS',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
            
        }  
        widgets={


            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event date'}),
            'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Poeple'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),

        }  

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ( 'name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_image')
        labels ={
             'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address':'' ,
            'venue_image':'',
        }  
        widgets={


            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip_code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Web Address'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
        }   