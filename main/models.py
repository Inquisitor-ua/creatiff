from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import TitleFieldPanel, FieldPanel
from wagtail.snippets.models import register_snippet

# Create your models here.
class ContactModel(models.Model):
    name = models.CharField(max_length=128, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=16, verbose_name="Phone number")
    message = models.TextField(verbose_name="Message text")
    datetime = models.DateTimeField(verbose_name="Date and time of the request", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Contact form"
        verbose_name_plural = "Contact forms"

class HomePage(Page):
    max_count = 1

    parent_page_types = ['wagtailcore.Page']

    content_panels = [
        TitleFieldPanel("title"),
        FieldPanel("slug"),
    ]

    subpage_types = []

    template = 'main/homepage.html'

@register_snippet
class HeaderSettings(models.Model):
    title = models.CharField(max_length=128, verbose_name="Title/name of the company")
    subtitle = models.CharField(max_length=128, verbose_name="Subtitle of the company")
    logo = models.ImageField(upload_to='header_logo/', verbose_name="Logo of the company")
    phone = models.CharField(max_length=16, verbose_name="Phone number")
    email = models.EmailField(verbose_name="Email")

    panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("logo"),
        FieldPanel("phone"),
        FieldPanel("email"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Header settings"

@register_snippet
class FooterSettings(models.Model):
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=16, verbose_name="Phone number")
    instagram_url = models.CharField(max_length=512, verbose_name="Instagram URL")
    facebook_url = models.CharField(max_length=512, verbose_name="Facebook URL")

    panels = [
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('instagram_url'),
        FieldPanel('facebook_url'),
    ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Footer settings"