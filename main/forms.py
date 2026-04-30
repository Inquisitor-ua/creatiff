from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label = "Ваше ім'я",
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введіть ваше ім'я"
        })
    )
    email = forms.CharField(
        label = "Ваша пошта",
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "email@example.com"
        })
    )
    phone = forms.CharField(
        label = 'Ваш телефон',
        required = False,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+34 951 392 250'
        })
    )
    message = forms.CharField(
        label = 'Ваше повідомлення',
        widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Опишіть ваше питання тут...',
            'rows': 4,
        })
    )
