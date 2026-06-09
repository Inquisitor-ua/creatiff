from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    ListBlock,
    TextBlock
)
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageBlock, ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
# from .snippets import HeaderSettings

# class HeaderSettingsBlock(blocks.StructBlock):
#     header = SnippetChooserBlock(HeaderSettings, label="Choose header settings")

#     class Meta:
#         template = "main/components/header_snippet.html"
#         icon = "title"
#         label = "Header"

class HeroStatsBlock(StructBlock):
    stats_number = CharBlock(max_length = 8, label = _("Statistics number"))
    stats_text = CharBlock(max_length = 64, label = _("Statistics text"))


class HeroBlock(StructBlock):
    caption_first_row = CharBlock(max_length = 128, label=_("First row of the caption"))
    caption_second_row = CharBlock(max_length = 128, label=_("Second row of the caption"))
    big_paragraph = CharBlock(max_length = 1024, label = _("Big text paragraph"))
    small_paragraph = CharBlock(max_length = 1024, label = _("Small text paragraph"))
    button = CharBlock(max_length = 64, label = _("Button text"))
    statistics = ListBlock(HeroStatsBlock(), label = _("Statistics"))
    image = ImageChooserBlock(required = False, label = _("Main hero image"))

    class Meta:
        template = "main/components/hero.html"
        label = _("Hero")


class PartenrInfoBlock(StructBlock):
    partner_logo = ImageChooserBlock(required=True, label = _("Partners logo"))
    partner_name = CharBlock(max_length = 256, label = _("Partners name"))


class PartnersBlock(StructBlock):
    title = CharBlock(max_length = 256, label = _("Partners section title"))
    partners = ListBlock(
        PartenrInfoBlock(required = False),
        label = _("Add partner"),
    )

    class Meta:
        template = 'main/components/partners.html'
        label = _("Partners")


class BannerBlock(StructBlock):
    heading = CharBlock(max_length = 256, label = _("Banner title"))
    button = CharBlock(max_length = 128, label = _("Banner button text"))

    class Meta:
        template = 'main/components/banner.html'
        label = _("Banner")


class PointsBlock(StructBlock):
    title = CharBlock(max_length = 128, label = _("Title of point"))
    text = CharBlock(max_length = 256, label = _("Text of point"))

    class Meta:
        label = _("Benefits")
        icon = 'pick'
    

class PromosectionBlock(StructBlock):
    title = CharBlock(max_length=250, label=_("Heading of a section"))
    description = TextBlock(label=_("Main description"))

    benefits = ListBlock(PointsBlock(), label=_("List of benefits"))

    cta_text = CharBlock(max_length=250, required=False, label=_("Text before button"))
    button_text = CharBlock(max_length=50, default=_("Contact with us"), label=_("Button text"))
    
    image = ImageChooserBlock(label=_("Image"), required=False, blank=True, null=True)

    class Meta:
        template = "main/components/promo_section.html"
        icon = "image-text"
        label = _("Promo-section")


# Blocks for content pages
class Images2p1Block(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = _("Add images"),
        min_num = 3,
        max_num = 3,
    )

    class Meta:
        icon = 'image'
        template = 'main/blocks/images2p1_block.html'
        label = _("2 + 1 images")


class Images3oversizedBlock(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = _("Add images"),
        min_num = 3,
        max_num = 3,
    )

    class Meta:
        icon = 'image'
        template = 'main/blocks/images3oversized_block.html'
        label = _("Row with 3 images")


class Images3p3Block(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = _("Add images"),
        min_num = 6,
        max_num = 6,
    )

    class Meta:
        icon = 'image'
        template = 'main/blocks/images3p3_block.html'
        label = _("2 rows with 3 images each")


class Images2Block(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = _("Add images"),
        min_num = 2,
        max_num = 2,
    )

    class Meta:
        icon = 'image'
        template = 'main/blocks/images2_block.html'
        label = _("Row with 2 images")


class GalleryBlock(StructBlock):
    title = CharBlock(max_length=250, label=_("Heading of a gallery"), blank=True, null=True)

    images = ListBlock(
        ImageChooserBlock(required = True),
        label = _("Add images"),
        min_num = 1,
    )

    class Meta:
        icon = "image"
        template = 'main/blocks/gallery_block.html'
        label = _("Gallery of images")


class Images3p2Block(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = _("Add images"),
        min_num = 5,
        max_num = 5,
    )

    class Meta:
        icon = 'image'
        template = 'main/blocks/images3p2_block.html'
        label = _("3 + 2 images")


class ImagetextBlock(StructBlock):
    layout = ChoiceBlock(
        choices=[
            ('img-left', _("Images on the left, text on the right")),
            ('img-right', _("Text on the left, images on the right")),
        ],
        default='img-left',
        label=_("Elements layout")
    )

    images = ListBlock(
        ImageChooserBlock(required = True),
        label = _("Add images"),
        min_num = 1,
    )

    text = RichTextBlock(label = _("Text"))

    class Meta:
        icon = "list-ul"
        template = "main/blocks/imagetext_block.html"
        label = _("Columns with images and text")