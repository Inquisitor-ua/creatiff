from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        label = "Su nombre",
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Escriban su nombre"
        })
    )
    email = forms.CharField(
        label = "Su correo electrónico",
        widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "email@example.com"
        })
    )
    phone = forms.CharField(
        label = 'Su teléfono',
        required = False,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+34 951 392 250'
        })
    )
    message = forms.CharField(
        label = 'Su mensaje',
        widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describa su consulta aquí...',
            'rows': 4,
        })
    )
