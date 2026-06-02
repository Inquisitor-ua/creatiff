from django.db import models

from wagtail.models import TranslatableMixin
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class HeaderSettings(models.Model):

    def get_context(self, request):
        context = super().get_context(request)
        wagtail_page = getattr(request, "current_page", None)
        context["page"] = wagtail_page
        return context

    class Meta:
        verbose_name = "Header settings"

@register_snippet
class FooterSettings(models.Model):
    caption = models.CharField(max_length=128, verbose_name="Footer caption")
    rights = models.CharField(max_length=128, verbose_name="Rights")

    panels = [
        FieldPanel('caption'),
        FieldPanel('rights'),
    ]

    def __str__(self):
        return self.caption or "Footer setting"

    class Meta:
        verbose_name = "Footer settings"

@register_snippet
class ContactFormSettings(TranslatableMixin, models.Model):
    title = models.CharField(max_length=128, verbose_name="Form title", blank=True)
    recipient_email = models.EmailField(blank=True, verbose_name="Email for receiving forms")

    phone_required = models.BooleanField(default=False, verbose_name="Is phone required")

    name_label = models.CharField(max_length=64, verbose_name="Label for field 'Name'", blank=True)
    name_placeholder = models.CharField(max_length=128, verbose_name="Placeholder for field 'Name'", blank=True)
    email_label = models.CharField(max_length=64, verbose_name="Label for field 'Email'", blank=True)
    email_placeholder = models.CharField(max_length=128, verbose_name="Placeholder for field 'Email'", blank=True)
    phone_label = models.CharField(max_length=64, verbose_name="Label for field 'Phone'", blank=True)
    phone_placeholder = models.CharField(max_length=128, verbose_name="Placeholder for field 'Phone'", blank=True)
    message_label = models.CharField(max_length=64, verbose_name="Label for field 'message'", blank=True)
    message_placeholder = models.CharField(max_length=256, verbose_name="Placeholder for field 'Message'", blank=True)
    submit_button_text = models.CharField(max_length=64, verbose_name="Confirmation button text", blank=True)
    success_message = models.CharField(max_length=256, verbose_name="Message for сonfirmation that the form was successfully submitted", blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('recipient_email'),
        FieldPanel('phone_required'),
        FieldPanel('name_label'),
        FieldPanel('name_placeholder'),
        FieldPanel('email_label'),
        FieldPanel('email_placeholder'),
        FieldPanel('phone_label'),
        FieldPanel('phone_placeholder'),
        FieldPanel('message_label'),
        FieldPanel('message_placeholder'),
        FieldPanel('submit_button_text'),
        FieldPanel('success_message'),
    ]

    def __str__(self):
        return self.title or "Contact form settings"

    class Meta:
        verbose_name = "Contact form settings"
        constraints = [
            models.UniqueConstraint(
                fields=('translation_key', 'locale'), 
                name='unique_translation_key_locale_main_contactformsettings'
            )
        ]
        