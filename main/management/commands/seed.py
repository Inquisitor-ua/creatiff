from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.core.files import File
from wagtail.models import Page, Site, Locale
from wagtail.images.models import Image 
from main.models import CompanySettings, HomePage, ContentPage
from main.snippets import ContactFormSettings

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
                # Content page 1
                'title': 'Construction, building and major refurbishments',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'Construction, building and major refurbishments',
                'preview_description': 'We manage construction projects from start to finish, taking every detail into account.',
                'stream_data': [
                    {"type": "rtfbody", "value": '<h2 data-block-key="2gnvd">Construction, building and major refurbishments</h2><p data-block-key="6uaf8"><b>Your dream home is our mission.</b></p><p data-block-key="cb3m">With Creatiff Star, construction becomes an art form. We don’t just build walls and a roof—we create a fully-fledged living space designed to meet your desires and needs.</p><p data-block-key="bg0v8"></p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="1fp6t">Why choose us? </h3><ul><li data-block-key="a51pl">A full range of services—from the groundbreaking to turnkey project completion.</li><li data-block-key="4fdst">A personalized approach—every project is unique, and we take all of the client’s wishes into account.</li><li data-block-key="drpca">Modern technologies — we use only proven materials and the latest construction solutions.</li><li data-block-key="9ne6h">Transparency and control — you are always kept informed of every stage of the work; we guarantee accountability and openness.</li><li data-block-key="c6tda">Punctuality — we deliver projects exactly on time, without delays or hidden costs.</li></ul>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="f2hq3"> Our services:</h3><ul><li data-block-key="dvoh8">Development of design proposals</li><li data-block-key="4hnsj">Design, approval, and project management</li><li data-block-key="dci8b">Full-cycle construction services—from foundation to turnkey completion</li><li data-block-key="5o9h2">MEP systems</li><li data-block-key="ldov">Landscape design</li></ul>'},
                    {"type": "rtfbody", "value": '<p data-block-key="f2hq3"><b>Creatiff Star</b> — we don’t just build. We create your dream home from the ground up. We don’t just construct buildings—we create comfort and trust.</p><p data-block-key="a170c">We are proud of our team of professionals—they are the foundation of our success and your satisfaction. It is a synergy of experience, knowledge, and a creative approach to every project.</p><p data-block-key="343iq">We don’t just work with residential real estate—we also carry out projects for hotels, restaurants, hostels, and industrial facilities!</p>'},
                ]
            },
            {
                # Content page 2
                'title': 'Painting and manufacture of metal structures',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'Painting and manufacture of metal structures',
                'preview_description': 'We create robust structures using state-of-the-art technology and high-quality materials for your projects.',
                'stream_data': [
                    {"type": "rtfbody", "value": '<h2 data-block-key="y20tp">Painting and fabrication of metal structures</h2><p data-block-key="fa29v">Every detail matters when it comes to creating a unique style for your home. We don’t just offer metal structures—we create works of art that transform spaces. Our products combine quality, style, and individuality. Work with us to create something special for your home, garden, or restaurant. </p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="kmeua">Unique metalwork:</h3><ul><li data-block-key="d9cse">For the home: Elegant railings, fences, and gates—each piece is custom-made to your specifications.</li><li data-block-key="6mg6b">For the garden: Unique benches, arches, and landscape sculptures that seamlessly complement any outdoor space.</li><li data-block-key="c76lp">For your yard: Reliable and aesthetically pleasing fences, pergolas, and decorative elements that will complement and enhance your property.</li><li data-block-key="50p9k">For restaurants: Exquisite metal structures for interiors and exteriors that will highlight the style and prestige of your establishment.</li></ul>'},
                    {"type": "images3oversized", "value": {'images': [
                        self.get_or_create_seed_image('content2_img1.png').id,
                        self.get_or_create_seed_image('content2_img2.png').id,
                        self.get_or_create_seed_image('content2_img3.png').id,
                    ]}},
                    {"type": "images3oversized", "value": {'images': [
                        self.get_or_create_seed_image('content2_img4.png').id,
                        self.get_or_create_seed_image('content2_img5.png').id,
                        self.get_or_create_seed_image('content2_img6.png').id,
                    ]}},
                    {"type": "rtfbody", "value": '<p data-block-key="tykyz">Working with us ensures that every detail will be executed to the highest standards of quality and design. We are dedicated to bringing your boldest ideas to life.</p><p data-block-key="5cn2c">Choose uniqueness—choose us!</p>'},
                    {"type": "images2p1", "value": {'images': [
                        self.get_or_create_seed_image('content2_img7.png').id,
                        self.get_or_create_seed_image('content2_img8.png').id,
                        self.get_or_create_seed_image('content2_img9.png').id,
                    ]}},
                ]
            },
            {
                # Content page 3
                'title': 'Modular homes',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'Modular homes',
                'preview_description': 'Our talented specialists transform shipping containers into modern, eco-friendly and functional spaces.',
                'stream_data': [
                    {"type": "rtfbody", "value": '<h2 data-block-key="6szf1">Modular homes</h2><p data-block-key="780gq"><b>Your dream home—anywhere in the world</b></p><p data-block-key="178ko">Do you want to live away from the hustle and bustle of the city, closer to nature and in the fresh air?Do you want to own a home that can be easily moved to another location if needed?Do you want to save on utility bills and live off the grid?</p><p data-block-key="7d693">If you answered “yes”—check out the idea of a self-sufficient modular home made from shipping containers!</p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="fqkn8">The Problem and the Solution</h3><p data-block-key="b5bhp">In the wake of the COVID-19 pandemic, many people are looking to live or vacation outside the city—away from the hustle and bustle. We offer homes built from shipping containers—durable, proven, modular, mobile, and self-sufficient.</p>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content3_img1.png').id},
                    {"type": "rtfbody", "value": '<h3 data-block-key="fqkn8">Why do people choose us?</h3><ul><li data-block-key="8rrtu">We build homes from shipping containers—reliable and proven structures.</li><li data-block-key="91uoq">We use a modular assembly method that allows us to create floor plans of any complexity.</li><li data-block-key="4uu9f">We ensure efficient transportation and installation anywhere.</li><li data-block-key="9pngq">We guarantee high-quality materials, insulation, and ventilation.</li><li data-block-key="58mu6">We equip the homes with life support systems for complete self-sufficiency—no need to connect to utility networks.</li></ul>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content3_img2.png').id},
                    {"type": "rtfbody", "value": '<h3 data-block-key="fqkn8">The advantages of our homes</h3><ul><li data-block-key="19s41">Excellent insulation, ensuring comfort in both winter and summer.</li><li data-block-key="2hlve">A modern ventilated facade system and high-quality windows—for a unique look.</li><li data-block-key="6p71f">Can be installed on both urban and rural plots—with lower costs and less red tape than conventional construction.</li><li data-block-key="293c9">If necessary, the house can be quickly moved to a new location.</li></ul>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content3_img3.png').id},
                    {"type": "rtfbody", "value": '<h3 data-block-key="fqkn8">Why are container homes cheaper than traditional construction?</h3><ul><li data-block-key="22uua">Speed of construction. Traditional construction takes much longer, which is why prefabricated homes are significantly cheaper.</li><li data-block-key="7k0ph">Less maintenance. All modules undergo factory testing, so you avoid unexpected costs after installation.</li><li data-block-key="alf0a">Quick return on investment. Fast construction = faster occupancy.</li><li data-block-key="fqqll">Savings on utility bills. Thanks to self-sufficiency and energy efficiency, you reduce your monthly expenses.</li></ul>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="fqkn8">How do we work?</h3><ul><li data-block-key="eesbf">You choose a plot of land, or we can help you find one.</li><li data-block-key="1id06">You choose a standard design or request a custom design and layout.</li><li data-block-key="10mqe">We manufacture, transport, and install your home.</li><li data-block-key="99m6s">You enjoy your finished, fully furnished home.</li></ul>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content3_img4.png').id},
                    {"type": "rtfbody", "value": '<h3 data-block-key="fqkn8">What will you get?</h3><ul><li data-block-key="15i98">A dream home that can be set up anywhere and moved if necessary.</li><li data-block-key="7useh">A self-contained home that doesn’t rely on utility networks.</li><li data-block-key="2020d">Comfort and safety all year round.</li><li data-block-key="2neja">A space that reflects your personality and style.</li></ul>'},
                    {"type": "images2", "value": {'images': [
                        self.get_or_create_seed_image('content3_img5.png').id,
                        self.get_or_create_seed_image('content3_img6.png').id,
                    ]}},
                    {"type": "rtfbody", "value": '<p data-block-key="fqkn8">We offer more than just a place to live—we give you free time. Time you can spend socializing, traveling, and loving—and we’ll take care of the house.</p>'},
                    {"type": "images2p1", "value": {'images': [
                        self.get_or_create_seed_image('content3_img7.png').id,
                        self.get_or_create_seed_image('content3_img8.png').id,
                        self.get_or_create_seed_image('content3_img9.png').id,
                    ]}},
                ]
            },
            {
                'title': 'Windows, doors, blinds and PVC products',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'Windows, doors, blinds and PVC products',
                'preview_description': 'Our range includes a variety of PVC products, as well as a wide selection of blinds to suit your taste.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>Windows, doors, blinds and PVC products</h1>"}]
            },
            {
                'title': 'Various household goods',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'Various household goods',
                'preview_description': 'We also specialise in products designed to make your everyday life more comfortable: from water filters to electric blankets.',
                'stream_data': [{"type": "rtfbody", "value": "<h1>Various household goods</h1>"}]
            },
            {
                'title': 'A wide range of furniture',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
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