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
    stats_number = CharBlock(max_length = 8, label = "Statistics number")
    stats_text = CharBlock(max_length = 64, label = "Statistics text")


class HeroBlock(StructBlock):
    caption_first_row = CharBlock(max_length = 128, label="First row of the caption")
    caption_second_row = CharBlock(max_length = 128, label="Second row of the caption")
    big_paragraph = CharBlock(max_length = 1024, label = 'Big text paragraph')
    small_paragraph = CharBlock(max_length = 1024, label = 'Small text paragraph')
    button = CharBlock(max_length = 64, label = "Button text")
    statistics = ListBlock(HeroStatsBlock(), label = "Statistics")
    image = ImageChooserBlock(required = False, label = "Main hero image")

    class Meta:
        template = "main/components/hero.html"
        label = "Hero"


class PartenrInfoBlock(StructBlock):
    partner_logo = ImageChooserBlock(required=True, label = "Partners logo")
    partner_name = CharBlock(max_length = 256, label = 'Partners name')


class PartnersBlock(StructBlock):
    partners = ListBlock(
        PartenrInfoBlock(required = False),
        label = 'Add partner',
    )

    class Meta:
        template = 'main/components/partners.html'
        label = 'Partners'


class BannerBlock(StructBlock):
    heading = CharBlock(max_length = 256, label = 'Banner title')
    button = CharBlock(max_length = 128, label = 'Banner button text')

    class Meta:
        template = 'main/components/banner.html'
        label = 'Banner'


class PointsBlock(StructBlock):
    title = CharBlock(max_length = 128, label = 'Title of point')
    text = CharBlock(max_length = 256, label = 'Text of point')

    class Meta:
        label = 'Benefits'
        icon = 'pick'
    

class PromosectionBlock(StructBlock):
    title = CharBlock(max_length=250, label="Heading of a section")
    description = TextBlock(label="Main description")

    benefits = ListBlock(PointsBlock(), label="List of benefits")

    cta_text = CharBlock(max_length=250, required=False, label="Text before button")
    button_text = CharBlock(max_length=50, default="Contact with us", label="Button text")
    
    image = ImageChooserBlock(label="Image")

    class Meta:
        template = "main/components/promo_section.html"
        icon = "image-text"
        label = "Promo-section"


class Images2p1Block(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = "Add images",
        min_num = 3,
        max_num = 3,
    )

    class Meta:
        icon = 'image'
        template = 'main/blocks/images2p1_block.html'
        label = "2 + 1 images"


class GalleryBlock(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = "Add images",
        min_num = 1,
    )

    class Meta:
        icon = "image"
        template = 'main/blocks/gallery.html'
        label = "Gallery of images"


class Images3p2Block(StructBlock):
    images = ListBlock(
        ImageChooserBlock(required = True),
        label = "Add images",
        min_num = 5,
        max_num = 5,
    )

    class Meta:
        icon = 'image'
        template = 'main/blocks/images3p2_block.html'
        label = "3 + 2 images"


class ImagetextBlock(StructBlock):
    layout = ChoiceBlock(
        choices=[
            ('img-left', 'Images on the left, text on the right'),
            ('img-right', 'Text on the left, images on the right'),
        ],
        default='img-left',
        label="Elements layout"
    )

    images = ListBlock(
        ImageChooserBlock(required = True),
        label = "Add images",
        min_num = 1,
    )

    text = RichTextBlock(label = 'Text')

    class Meta:
        icon = "list-ul"
        template = "main/blocks/imagetext_block.html"
        label = "Columns with images and text"