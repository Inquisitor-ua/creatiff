from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from .models import ContactModel, HomePage

def process_contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            #Дописати валідацію форми та збереження в БД
            form_data = form.cleaned_data
            ContactModel.objects.create(name = form_data['name'], email = form_data['email'], phone = form_data['phone'], message = form_data['message'])
    return redirect(request.META.get('HTTP_REFERER', HomePage.objects.live().first().url))

def index(request):
    return render(request, 'main/index.html')
def homepage(request):
    return render(request, 'main/homepage.html')
