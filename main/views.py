from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from .models import ContactModel, HomePage
from .snippets import ContactFormSettings

def process_contact_form(request):
    form_settings = None

    if request.method == 'POST':
        form_settings = ContactFormSettings.objects.first()

        form = ContactForm(request.POST, settings=form_settings)
        if form.is_valid():
            form_data = form.cleaned_data
            ContactModel.objects.create(
                name=form_data.get('name', ''),
                email=form_data.get('email', ''),
                phone=form_data.get('phone', ''),
                message=form_data.get('message', ''),
            )
    else:
        form = ContactForm(settings=form_settings)

    return redirect(request.META.get('HTTP_REFERER', HomePage.objects.live().first().url))

def index(request):
    return render(request, 'main/index.html')
def homepage(request):
    return render(request, 'main/homepage.html')
