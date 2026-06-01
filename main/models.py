from django.db import models

from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, ObjectList, TabbedInterface
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from . import blocks

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

    #Hero
    hero = StreamField([
        ('hero', blocks.HeroBlock())
    ], use_json_field=True, blank=True)

    #Content pages tiles
    details_button = models.CharField(max_length=64, verbose_name="Details button")

    #Partners
    partners = StreamField([
        ('partners', blocks.PartnersBlock()),
    ], use_json_field=True, blank=True)

    #Banner
    banner = StreamField([
        ('banner', blocks.BannerBlock()),
    ], use_json_field=True, blank=True)

    #Promo section
    promo = StreamField([
        ('promo', blocks.PromosectionBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero'),
        ], heading = "Hero settings (First banner)"),
        MultiFieldPanel([
            FieldPanel('details_button'),
        ], heading = "Content pages tiles settings"),
        MultiFieldPanel([
            FieldPanel('partners'),
        ], heading = "List of partners"),
        MultiFieldPanel([
            FieldPanel('banner'),
        ], heading = "Banner settings"),
        MultiFieldPanel([
            FieldPanel('promo'),
        ], heading = "Promo-section"),
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
        ('rtfbody', RichTextBlock()),
        ('images2p1', blocks.Images2p1Block()),
        ('images3p2', blocks.Images3p2Block()),
        ('gallery', blocks.GalleryBlock()),
        ('imagestext', blocks.ImagetextBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("preview_title"),
        FieldPanel("preview_image"),
        FieldPanel("preview_description"),
        FieldPanel("body"),
    ]

    subpage_types = []

    template = 'main/page.html'


@register_setting
class CompanySettings(BaseSiteSetting):
    # Overall information
    title = models.CharField(max_length=128, verbose_name="Title/name of the company")
    subtitle = models.CharField(max_length=128, verbose_name="Subtitle of the company")

    # Contacts
    phone = models.CharField(max_length=50, blank=True, verbose_name="Phone")
    email = models.EmailField(blank=True, verbose_name="Email")

    # Social media
    facebook = models.URLField(blank=True, verbose_name="Facebook URL")
    instagram = models.URLField(blank=True, verbose_name="Instagram URL")

    # Photos
    logo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Website logo")
    favicon = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name="Website favicon")

    overall = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('subtitle'),
        ])
    ]

    contact_panels = [
        MultiFieldPanel([
            FieldPanel('phone'),
            FieldPanel('email'),
        ], heading="Contact information")
    ]

    social_panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
        ], heading="Social media URLs")
    ]

    photos = [
        FieldPanel('logo'),
        FieldPanel('favicon')
    ]

    edit_handler = TabbedInterface([
        ObjectList(overall, heading="Overall information"),
        ObjectList(photos, heading="Website important images"),
        ObjectList(contact_panels, heading="Contacts"),
        ObjectList(social_panels, heading="Social media"),
    ])

    class Meta:
        verbose_name = "Company information"