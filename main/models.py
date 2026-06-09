from django.db import models
from django.utils.translation import gettext_lazy as _

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
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=16, verbose_name=_("Phone number"))
    message = models.TextField(verbose_name=_("Message text"))
    datetime = models.DateTimeField(verbose_name=_("Date and time of the request"), auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = _("Contact form")
        verbose_name_plural = _("Contact forms")


# Pages
class HomePage(Page):
    max_count = 1

    parent_page_types = ['wagtailcore.Page']

    #Hero
    hero = StreamField([
        ('hero', blocks.HeroBlock())
    ], use_json_field=True, blank=True)

    #Content pages tiles
    details_button = models.CharField(max_length=64, verbose_name="Details button", default="Details")
    load_more_button = models.CharField(max_length=64, verbose_name="Button for loading more tiles (only on phones)", default="Load More")

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
        ], heading = _("Hero settings (First banner)")),
        MultiFieldPanel([
            FieldPanel('details_button'),
        ], heading = _("Content pages tiles settings")),
        MultiFieldPanel([
            FieldPanel('partners'),
        ], heading = _("List of partners")),
        MultiFieldPanel([
            FieldPanel('banner'),
        ], heading = _("Banner settings")),
        MultiFieldPanel([
            FieldPanel('promo'),
        ], heading = _("Promo-section")),
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

    preview_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name=_("Preview card image"))
    preview_title = models.CharField(max_length=256, verbose_name=_("Preview card title"))
    preview_description = models.CharField(max_length=512, verbose_name=_("Preview card description"))

    body = StreamField([
        ('image', ImageChooserBlock()),
        ('rtfbody', RichTextBlock(label=_("Text editor"))),
        ('images2p1', blocks.Images2p1Block()),
        ('images3p2', blocks.Images3p2Block()),
        ('images3oversized', blocks.Images3oversizedBlock()),
        ('images3p3', blocks.Images3p3Block()),
        ('images2', blocks.Images2Block()),
        ('gallery', blocks.GalleryBlock()),
        ('imagestext', blocks.ImagetextBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("preview_title"),
            FieldPanel("preview_image"),
            FieldPanel("preview_description"),
        ], heading = _("Preview card information"), help_text = _("This summary card will appear on the home page")),
        FieldPanel("body"),
    ]

    subpage_types = []

    template = 'main/page.html'


@register_setting
class CompanySettings(BaseSiteSetting):
    # Overall information
    title = models.CharField(max_length=128, verbose_name=_("Title/name of the company"))
    subtitle = models.CharField(max_length=128, verbose_name=_("Subtitle of the company"))

    # Contacts
    phone = models.CharField(max_length=50, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    recipient_email = models.EmailField(blank=True, verbose_name=_("Email for receiving forms"))

    # Social media
    facebook = models.URLField(blank=True, verbose_name=_("Facebook URL"))
    instagram = models.URLField(blank=True, verbose_name=_("Instagram URL"))

    # Photos
    logo = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name=_("Website logo"))
    favicon = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name=_("Website favicon"))

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
            FieldPanel('recipient_email'),
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
        ObjectList(overall, heading=_("Overall information")),
        ObjectList(photos, heading=_("Website important images")),
        ObjectList(contact_panels, heading=_("Contacts")),
        ObjectList(social_panels, heading=_("Social media")),
    ])

    class Meta:
        verbose_name = _("Company information")