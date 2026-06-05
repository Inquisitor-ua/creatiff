from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files import File
from wagtail.models import Page, Site, Locale
from wagtail.images.models import Image 
from main.models import CompanySettings, HomePage, ContentPage
from main.snippets import ContactFormSettings
from django.conf import settings

import os


class Command(BaseCommand):
    help = "Automatically creates a homepage, default site setup, and populates content pages."

    def get_or_create_seed_image(self, filename):
        file_path = os.path.join("media", "original_images", filename)
        self.stdout.write(file_path)
        
        if not os.path.exists(file_path):
            return None
            
        image = Image.objects.filter(title=filename).first()
        
        if not image:
            with open(file_path, "rb") as f:
                image = Image.objects.create(
                    title=filename,
                    file=File(f, name=filename)
                )
            
        return image

    def ensure_homepage_hero(self, homepage, image_id):
        hero_payload = [
            {
                "type": "hero",
                "value": {
                    "caption_first_row": "STAR CREATIFF",
                    "caption_second_row": "We do everything",
                    "big_paragraph": "Our company was founded to fulfill all of our clients’ creative ideas and wishes. We’ll manufacture and install everything you have in mind right here in our own facility.",
                    "small_paragraph": "We implement all technical solutions.",
                    "button": "Bring the Idea to Life",
                    "statistics": [
                        {"stats_number": "9K", "stats_text": "Happy Customers"},
                        {"stats_number": "2K", "stats_text": "Furniture Sold"},
                        {"stats_number": "28", "stats_text": "Completed Structures"},
                    ],
                    "image": image_id,
                },
            }
        ]

        try:
            current = getattr(homepage, 'hero', None)
            is_empty = not current or len(current) == 0
            if is_empty:
                homepage.hero = hero_payload
                homepage.save_revision().publish()
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to set hero block: {e}'))

    def ensure_homepage_banner(self, homepage):
        banner_payload = [
            {
                "type": "banner", 
                "value": {
                    "heading": "Are you interested in our offers?",
                    "button": "Contact a consultant",
                }
            }
        ]

        try:
            current = getattr(homepage, 'banner', None)
            is_empty = not current or len(current) == 0
            if is_empty:
                homepage.banner = banner_payload
                homepage.save_revision().publish()
                self.stdout.write(self.style.SUCCESS("Successfully populated Banner on HomePage."))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to set banner block: {e}'))

    def ensure_homepage_partners(self, homepage, image_id):
        if not image_id:
            self.stdout.write(self.style.WARNING("Skipping Partners block setup: No images found in DB."))
            return

        partners_payload = [
            {
                "type": "partners",
                "value": {
                    "partners": [
                        {"partner_logo": image_id, "partner_name": "Fraves 1"},
                        {"partner_logo": image_id, "partner_name": "Fraves 2"},
                        {"partner_logo": image_id, "partner_name": "Fraves 3"},
                        {"partner_logo": image_id, "partner_name": "Fraves 4"},
                        {"partner_logo": image_id, "partner_name": "Fraves 5"},
                        {"partner_logo": image_id, "partner_name": "Fraves 6"},
                        {"partner_logo": image_id, "partner_name": "Fraves 7"},
                        {"partner_logo": image_id, "partner_name": "Fraves 8"},
                    ],
                    "title": "Our partners"
                }
            }
        ]

        try:
            current = getattr(homepage, 'partners', None)
            is_empty = not current or len(current) == 0
            if is_empty:
                homepage.partners = partners_payload
                homepage.save_revision().publish()
                self.stdout.write(self.style.SUCCESS("Successfully populated Partners block on HomePage."))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to set partners block: {e}'))

    def ensure_homepage_promo(self, homepage, image_id):
        promo_payload = [
            {
                "type": "promo",
                "value": {
                    "title": "We can create anything you want!",
                    "description": "Whether you're looking for custom furniture for your home or office, we're here to bring your vision to life. Send us a picture from Pinterest, and we'll create unique, custom-made furniture that perfectly matches your preferences and style.",
                    "benefits": [
                        {
                            "title": "Personalized approach", 
                            "text": "We listen to your needs and take all your requests into account."
                        },
                        {
                            "title": "Creativity", 
                            "text": "We combine and adapt concepts to create masterpieces."
                        },
                        {
                            "title": "Responsibility", 
                            "text": "We adhere to the specified deadlines for our work."
                        },
                    ],
                    "cta_text": "Tell us what you're looking for, and we'll make it happen. Check out our portfolio!",
                    "button_text": "Contact us",
                    "image": image_id,
                }
            }
        ]

        try:
            current = getattr(homepage, 'promo', None)
            is_empty = not current or len(current) == 0
            if is_empty:
                homepage.promo = promo_payload
                homepage.save_revision().publish()
                self.stdout.write(self.style.SUCCESS("Successfully populated Promo-section on HomePage."))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to set promo block: {e}'))

    def ensure_contact_form_settings(self):
        default_locale = Locale.get_default()

        defaults = {
            "title": "HAVE ANY QUESTIONS? CONTACT US",
            "recipient_email": "star.creatiff@gmail.com",
            "phone_required": False,

            "name_label": "Your name",
            "name_placeholder": "Enter your name",
            
            "email_label": "Your Email",
            "email_placeholder": "example@gmail.com",
            
            "phone_label": "Your phone",
            "phone_placeholder": "+34 123 456 789",
            
            "message_label": "Your message",
            "message_placeholder": "Describe your question here...",
            
            "submit_button_text": "Send a Letter",
            "success_message": "Your message has been sent successfully!",
        }

        obj, created = ContactFormSettings.objects.update_or_create(
            locale=default_locale,
            defaults=defaults,
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Successfully created ContactFormSettings snippet."))
        else:
            self.stdout.write("ContactFormSettings snippet already exists.")

    def ensure_company_settings(self, site):
        try:
            image = self.get_or_create_seed_image('default_logo.png')
        except Exception as e:
            image = None
            self.stdout.write(f"Error: {e}")

        defaults = {
            'title': "STAR Creatiff",
            'subtitle': "realizamos ideas",
            'phone': "+34 644 82 59 83",
            'email': "star.creatiff@gmail.com",
            'facebook': "https://facebook.com",
            'instagram': "https://instagram.com",
            'logo': image,
            'favicon': image,
        }

        CompanySettings.objects.update_or_create(
            site=site,
            defaults=defaults,
        )

    def handle(self, *args, **options):
        root_page = Page.objects.get(id=1)

        if not HomePage.objects.exists():
            homepage = HomePage(
                title="Homepage",
                slug="homepage",
                live=True,
                details_button="Details",
            )
            root_page.add_child(instance=homepage)
            self.stdout.write(self.style.SUCCESS("Successfully created HomePage."))
        else:
            homepage = HomePage.objects.first()
            self.stdout.write("HomePage already exists.")

        site = Site.objects.filter(is_default_site=True).first()
        if site:
            if site.root_page != homepage:
                site.root_page = homepage
                site.save()
        else:
            site = Site.objects.create(
                hostname="localhost",
                port=8000,
                root_page=homepage,
                is_default_site=True,
            )

        self.ensure_company_settings(site)

        try:
            image_id = self.get_or_create_seed_image('photo_block_1.png').id
            self.ensure_homepage_hero(homepage, image_id)
        except Exception as e:
            self.stdout.write(f"Error: {e}")

        try:
            self.ensure_homepage_banner(homepage)
        except Exception as e:
            self.stdout.write(f"Error: {e}")

        try:
            image_id = self.get_or_create_seed_image('partner.png').id
            self.ensure_homepage_partners(homepage, image_id)
        except Exception as e:
            self.stdout.write(f"Error: {e}")

        try:
            image_id = self.get_or_create_seed_image('photo_block_1.png').id
            self.ensure_homepage_promo(homepage, image_id)
        except Exception as e:
            self.stdout.write(f"Error: {e}")

        try:
            self.ensure_contact_form_settings()
        except Exception as e:
            self.stdout.write(f"Error: {e}")

        Page.objects.filter(slug="home").delete()

        pages_data = [
            {
                'title': 'Construction, building and major refurbishments',
                'preview_title': 'Construction, building and major refurbishments',
                'preview_description': 'We manage construction projects from start to finish, taking every detail into account.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>Construction, building and major refurbishments</h1>"}]
            },
            {
                'title': 'Painting and manufacture of metal structures',
                'preview_title': 'Painting and manufacture of metal structures',
                'preview_description': 'We create robust structures using state-of-the-art technology and high-quality materials for your projects.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>Painting and manufacture of metal structures</h1>"}]
            },
            {
                'title': 'Modular homes',
                'preview_title': 'Modular homes',
                'preview_description': 'Our talented specialists transform shipping containers into modern, eco-friendly and functional spaces.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>Modular homes</h1>"}]
            },
            {
                'title': 'Windows, doors, blinds and PVC products',
                'preview_title': 'Windows, doors, blinds and PVC products',
                'preview_description': 'Our range includes a variety of PVC products, as well as a wide selection of blinds to suit your taste.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>Windows, doors, blinds and PVC products</h1>"}]
            },
            {
                'title': 'Various household goods',
                'preview_title': 'Various household goods',
                'preview_description': 'We also specialise in products designed to make your everyday life more comfortable: from water filters to electric blankets.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>Various household goods</h1>"}]
            },
            {
                'title': 'A wide range of furniture',
                'preview_title': 'A wide range of furniture',
                'preview_description': 'We offer modern, stylish furniture for the home, office and commercial spaces. Choose quality and comfort in every element of your interior.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>A wide range of furniture</h1>"}]
            },
        ]

        for page in pages_data:
            generated_slug = slugify(page['title'])

            if not ContentPage.objects.filter(slug=generated_slug).exists():
                new_page = ContentPage(
                    title=page['title'],
                    slug=generated_slug,
                    preview_title=page['preview_title'],
                    preview_description=page['preview_description'],
                    body=page['stream_data'],
                )
                
                homepage.add_child(instance=new_page)
                new_page.save_revision().publish()
                self.stdout.write(self.style.SUCCESS(f"Created ContentPage: {page['title']}"))