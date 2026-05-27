from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock
from wagtail.fields import RichTextField, StreamField

# from .blocks import HeaderSettingsBlock

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


# Pages
class HomePage(Page):
    max_count = 1

    parent_page_types = ['wagtailcore.Page']

    body = StreamField([
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    subpage_types = ['main.ContentPage']

    template = 'main/homepage.html'

    def get_context(self, request):
        context = super().get_context(request)
        posts = ContentPage.objects.live().filter(locale=self.locale)
        context['posts'] = posts
        return context

class ContentPage(Page):
    parent_page_types = ['main.HomePage']

    preview_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Preview card image")
    preview_title = models.CharField(max_length=256, verbose_name='Preview card title')
    preview_description = models.CharField(max_length=512, verbose_name="Preview card description")

    body = StreamField([
        ('image', ImageChooserBlock()),
        ('rtfbody', RichTextBlock())
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("preview_title"),
        FieldPanel("preview_image"),
        FieldPanel("preview_description"),
        FieldPanel("body"),
    ]

    subpage_types = []

    template = 'main/page.html'