from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import FormView
from django.contrib import messages
from django.utils.translation import get_language

from wagtail.models import Locale

from .forms import ContactForm
from .models import ContactModel, HomePage
from .snippets import ContactFormSettings


class ProcessContactFormView(FormView):
    form_class = ContactForm

    def get_current_locale(self):
        current_lang = get_language()
        return Locale.objects.filter(language_code=current_lang).first()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        current_locale = self.get_current_locale()
        kwargs['settings'] = ContactFormSettings.objects.filter(locale=current_locale).first()
        return kwargs

    def form_valid(self, form):
        current_locale = self.get_current_locale()
        form_settings = ContactFormSettings.objects.filter(locale=current_locale).first()
        form_data = form.cleaned_data
        contact = ContactModel.objects.create(
            name = form_data.get('name', ''),
            email = form_data.get('email', ''),
            phone = form_data.get('phone', ''),
            message = form_data.get('message', ''),
        )

        if form_settings and form_settings.success_message:
            success_msg = form_settings.success_message
        else:
            success_msg = _("Message has been successfully sent")

        messages.success(self.request, success_msg)
        return redirect(self.get_success_redirect_url())
    
    def form_invalid(self, form):
        current_locale = self.get_current_locale()
        form_settings = ContactFormSettings.objects.filter(locale=current_locale).first()

        if form_settings and form_settings.error_message:
            error_msg = form_settings.error_message
        else:
            error_msg = _("An error occurred while sending the message")

        messages.error(self.request, error_msg)
        return redirect(self.get_success_redirect_url())
    
    # AI slop
    def get_success_redirect_url(self):
        referer = self.request.META.get('HTTP_REFERER')
        if referer:
            return referer

        current_locale = self.get_current_locale()
        home_page = HomePage.objects.live().filter(locale=current_locale).first()
        
        if home_page:
            return home_page.get_url(self.request)
            
        return '/'



