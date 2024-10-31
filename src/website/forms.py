from django import forms
from .models import ContactUs

class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message', 'phone', 'budget']

        labels = {
            'name': '',
            'email': '',
            'message': '',
            'phone': '',
            'budget': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Your Message'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Your Phone Number'}),
            'budget': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Your Budget'}),
        }


