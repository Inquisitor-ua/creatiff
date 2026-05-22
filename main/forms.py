from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label = "Your name",
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter your name"
        })
    )
    email = forms.CharField(
        label = "Your email",
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "email@example.com"
        })
    )
    phone = forms.CharField(
        label = 'Your phone',
        required = False,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+34 951 392 250'
        })
    )
    message = forms.CharField(
        label = 'Your message',
        widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Please describe your question here...',
            'rows': 4,
        })
    )
