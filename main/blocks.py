from wagtail.blocks import (
    CharBlock,
    ChoiceBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    ListBlock
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