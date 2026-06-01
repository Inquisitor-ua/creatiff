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
        return self.caption

    class Meta:
        verbose_name = "Footer settings"