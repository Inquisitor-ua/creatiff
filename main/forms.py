from django import forms
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.settings = kwargs.pop('settings', None)
        super().__init__(*args, **kwargs)

        self.fields['name'].label = getattr(self.settings, 'name_label', '') or _("Your name")
        self.fields['name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': getattr(self.settings, 'name_placeholder', '') or _("Input your name")
        })

        self.fields['email'].label = getattr(self.settings, 'email_label', '') or _("Your Email")
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': getattr(self.settings, 'email_placeholder', '') or _("email@example.com")
        })


        self.fields['phone'].label = getattr(self.settings, 'phone_label', '') or _("Your phone")
        self.fields['phone'].required = getattr(self.settings, 'phone_required', False)
        self.fields['phone'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': getattr(self.settings, 'phone_placeholder', '') or "+34 123 456 789"
        })

        self.fields['message'].label = getattr(self.settings, 'message_label', '') or _("Your message")
        self.fields['message'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': getattr(self.settings, 'message_placeholder', '') or _("Describe your question here"),
            'rows': 4,
        })
