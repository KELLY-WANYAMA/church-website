from django import forms
from .models import CustomerReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or "@" not in email:
            raise forms.ValidationError("Please enter a valid email address.")
        return email
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if not message or len(message) < 1:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message
    