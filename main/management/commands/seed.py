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
        file_path = os.path.join("media", "seed_images", filename)
        
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
            "error_message": "Some error has been occured, please try later",
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
                    {"type": "images3p3", "value": {'images': [
                        self.get_or_create_seed_image('content2_img1.png').id,
                        self.get_or_create_seed_image('content2_img2.png').id,
                        self.get_or_create_seed_image('content2_img3.png').id,
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
                # Content page 4
                'title': 'Windows, doors, blinds and PVC products',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'Windows, doors, blinds and PVC products',
                'preview_description': 'Our range includes a variety of PVC products, as well as a wide selection of blinds to suit your taste.',
                'stream_data': [
                    {"type": "rtfbody", "value": '<h2 data-block-key="viric">Windows, doors, blinds and PVC products</h2><p data-block-key="4e25s">Welcome to the world of windows and doors from the best manufacturers in Ukraine and Europe! We are an official distributor of automatic windows and doors. Our company has not only 15 years of successful operation in Ukraine, but also five years of experience in the European market. We are proud to continuously expand our capabilities, keep up with global technological trends, and update our equipment to offer our customers the very best.</p><p data-block-key="8kkk0"></p><p data-block-key="70heo">What makes our products special?</p><ol><li data-block-key="47gie">Quality: Our products are manufactured using professional German and Austrian equipment. We use only high-quality materials from renowned European manufacturers, such as Gealan profiles (Germany), Siegenia window hardware (Germany), Guardian glass (Germany), Pilkington (UK), and others.</li><li data-block-key="8r1v1">Certification and Standards: Our production is certified in accordance with the ISO 9001:2009 “Quality Management Systems” standard. In addition, our products are manufactured in accordance with European EN standards. We not only meet these standards but exceed them.</li></ol>'},
                    {"type": "images4", "value": {'images': [
                        self.get_or_create_seed_image('content4_img1.png').id,
                        self.get_or_create_seed_image('content4_img2.png').id,
                        self.get_or_create_seed_image('content4_img3.png').id,
                        self.get_or_create_seed_image('content4_img4.png').id,
                    ]}},
                    {"type": "rtfbody", "value": '<p data-block-key="h2ox2">Create a cozy and comfortable atmosphere in your home with our windows and doors! We offer a wide range of products for private homes, cottages, and apartments. Our windows not only keep you warm in the winter and cool in the summer, but also protect your home from outside noise and potential intruders. PVC windows are a practical and durable solution that harmoniously complements your home’s facade. They require no special maintenance and give your home an elegant and modern look. We are ready to meet your highest expectations by bringing light, safety, and comfort into your home. All you have to do is choose.</p>'},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content4_img5.png').id,
                        ],
                        'text': '<ul><li data-block-key="h2ox2">Thermal insulation: 1.07 m² °C/W</li><li data-block-key="eqook">Sound insulation: up to 42 dB</li><li data-block-key="1f1gg">Installation depth: 82.5 mm</li><li data-block-key="8or5g">Number of chambers: 6</li><li data-block-key="61ila">Glazing thickness: 32, 44, 48 mm</li><li data-block-key="cuf7c">Seal color: gray</li><li data-block-key="3f6it">Profile manufacturer: Germany</li></ul>'
                    }},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content4_img6.png').id,
                        ],
                        'text': '<ul><li data-block-key="h2ox2">Thermal insulation: 0.91 m² °C/W</li><li data-block-key="5u0r">Sound insulation: up to 38 dB</li><li data-block-key="46l2i">Installation depth: 70 mm</li><li data-block-key="dp0aa">Number of chambers: 6</li><li data-block-key="1n684">Glass panes: 24, 32, 42 mm</li><li data-block-key="e9mqr">Seal color: gray; black for laminated structures</li><li data-block-key="jc76">Profile manufacturer: Ukraine</li></ul>'
                    }},
                    {"type": "rtfbody", "value": '<h3 data-block-key="h2ox2">SWS Sliding System</h3><p data-block-key="afgjq">The SWS sliding system is the perfect solution for glazing loggias, balconies, conservatories, and sunrooms. It is also suitable for office partitions, saving space and increasing usable floor area.</p>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content4_img7.png').id},
                    {"type": "rtfbody", "value": '<p data-block-key="h2ox2">Key advantages of SWS:</p><ul><li data-block-key="4ic0k">Reliability and durability thanks to a multi-chamber PVC profile and metal reinforcement.</li><li data-block-key="41gg1">Smooth sash operation thanks to aluminum guides and roller carriages.</li><li data-block-key="ajjl">High airtightness and moisture protection thanks to double brush seals.</li><li data-block-key="d2j9d">Energy savings: the plastic profile is 30–40% warmer than aluminum.</li><li data-block-key="2gpgm">Option to install an easily removable mosquito screen.</li></ul>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content4_img8.png').id},
                    {"type": "rtfbody", "value": '<p data-block-key="h2ox2">SWS offers a stylish, modern look and excellent value for money. Choose SWS for maximum comfort and efficiency!</p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="h2ox2">Here you can choose windows to suit any style:</h3><p data-block-key="bgqc3">Arched, round, laminated, and transom windows.</p>'},
                    {"type": "images2p1", "value": {'images': [
                        self.get_or_create_seed_image('content4_img9.png').id,
                        self.get_or_create_seed_image('content4_img10.png').id,
                        self.get_or_create_seed_image('content4_img11.png').id,
                    ]}},
                    {"type": "rtfbody", "value": '<p data-block-key="h2ox2">It’s not just classic white—Viknar\'off manufactures windows in a wide range of colors—from classic browns to vibrant shades—using high-quality PVC film. This allows you to choose the best options for every facade. Laminated films do not fade or crack in the sun or cold, and the windows retain their attractive appearance for longer. These windows require no special maintenance other than periodic cleaning to remove dirt and dust.</p>'},
                    {"type": "gallery", "value": {'title': 'Colors:', 'images': [
                        self.get_or_create_seed_image('content4_img12.png').id,
                        self.get_or_create_seed_image('content4_img13.png').id,
                        self.get_or_create_seed_image('content4_img14.png').id,
                        self.get_or_create_seed_image('content4_img15.png').id,
                        self.get_or_create_seed_image('content4_img12.png').id,
                    ]}},
                    {"type": "image", "value": self.get_or_create_seed_image('content4_img16.png').id},
                    {"type": "rtfbody", "value": '<p data-block-key="h2ox2">Doors are not just a form of protection; they are also the calling card of your home. That is why they must be not only reliable, but also elegant and unique. This is exactly what we offer our customers. You can order standard doors as well as arched doors, sliding doors, and folding (accordion-style) doors.</p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="h2ox2">What can you find here?</h3><h4 data-block-key="81fhd">Standard doors</h4><p data-block-key="e5vs">Simplicity and reliability—the perfect solution for those who appreciate classic elegance.</p>'},
                    {"type": "images2", "value": {'images': [
                        self.get_or_create_seed_image('content4_img17.png').id,
                        self.get_or_create_seed_image('content4_img18.png').id,
                    ]}},
                    {"type": "gallery", "value": {'title': 'Standard Door Gallery', 'images': [
                        self.get_or_create_seed_image('content4_img19.png').id,
                        self.get_or_create_seed_image('content4_img20.png').id,
                        self.get_or_create_seed_image('content4_img21.png').id,
                        self.get_or_create_seed_image('content4_img22.png').id,
                    ]}},
                    {"type": "gallery", "value": {'title': 'Gallery of Double Doors', 'images': [
                        self.get_or_create_seed_image('content4_img23.png').id,
                        self.get_or_create_seed_image('content4_img24.png').id,
                        self.get_or_create_seed_image('content4_img25.png').id,
                        self.get_or_create_seed_image('content4_img23.png').id,
                    ]}},
                    {"type": "rtfbody", "value": '<h3 data-block-key="h2ox2">Arched doors:</h3><p data-block-key="8pieq">Elegant and sophisticated, they will add a special touch to your interior.</p>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content4_img26.png').id},
                    {"type": "rtfbody", "value": '<h3 data-block-key="h2ox2">Parallel sliding doors:</h3><p data-block-key="3mgic">Space is a valuable resource. Our doors will help you make the most of it.</p>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content4_img27.png').id},
                    {"type": "rtfbody", "value": '<h2 data-block-key="h2ox2">Choose a door that reflects your style and creates a unique atmosphere in your home.</h2><p data-block-key="d81on">Entrust your doors to us, and they will not only protect you but also serve as a calling card for your cozy home.</p><p data-block-key="44oku"></p><p data-block-key="705tt">By choosing our company, you’re guaranteed not only the highest product quality but also fast delivery. We value your time and ensure fast and secure delivery. We also handle the entire installation process, offering you a hassle-free experience from start to finish. And, of course, our ten-year product warranty confirms our commitment to long-term quality and your trust. Choose our company and let quality become a part of your life.</p>'},
                ]
            },
            {
                # Content page 5
                'title': 'Various household goods',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'Various household goods',
                'preview_description': 'We also specialise in products designed to make your everyday life more comfortable: from water filters to electric blankets.',
                'stream_data': [
                    {"type": "rtfbody", "value": '<h2 data-block-key="ezvu7">Various household items</h2><h3 data-block-key="cpq5e">Water filters</h3><p data-block-key="4bsmi">Clean water is essential for health and comfort. It plays a key role in our homes, and using filters isn’t just a trend—it’s a genuine necessity. Let’s explore why installing a filter is a wise decision.</p><ol><li data-block-key="1g0mg">Family Health: Filters provide clean water free of chlorine, heavy metals, and bacteria. This means you and your family are drinking water that supports your health and well-being.</li><li data-block-key="ft5g5">Save Time and Money: Forget about buying bottled water! By installing a filter, you’ll save money and time, and reduce your environmental impact.</li><li data-block-key="6gqtt">Environmental responsibility: By using filters, you reduce your consumption of plastic bottles, helping to preserve nature. It’s a small step that makes a big difference.</li></ol><p data-block-key="fqhfn">Don’t miss the opportunity to provide your home with clean water—install a filter today!</p>'},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content5_img1.png').id,
                            self.get_or_create_seed_image('content5_img2.png').id,
                            self.get_or_create_seed_image('content5_img3.png').id,
                        ],
                        'text': '<p data-block-key="mskng"><b>Versatile flow-through filter for deep purification of moderately hard water</b></p><p data-block-key="aj0ca">The cartridges purify the water in stages: first removing visible mechanical impurities, and then dissolved harmful substances. The pre-filtration stage traps particles as small as 5 microns. The second stage softens the water, preventing limescale buildup in the kettle. The third stage provides final filtration—down to 0.8 microns (which is 125 times thinner than a human hair).</p><p data-block-key="446l0">The AQUALEN ion-exchange carbon fiber reliably captures and retains heavy metals and other hazardous impurities often found in tap water.</p><p data-block-key="binrq">Cristal H purifies water at a rate of 2 liters per minute—a glass of clean water fills in 10 seconds.Use the filter to prepare food of any volume—from baby purees to soups and beverages.</p><p data-block-key="91gtm">In our catalog, you’ll find both the filters themselves and all the necessary accessories.</p><p data-block-key="8s8b"></p>'
                    }},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content5_img4.png').id,
                        ],
                        'text': '<h3 data-block-key="x25ux">The perfect choice for your kitchen!</h3><p data-block-key="f3bk1">This versatile filter with a separate faucet is ideal for small kitchens, avid cooks, practical people, and those who appreciate a proven approach.Triple filtration system:</p><ul><li data-block-key="aqf7b">K3 cartridge: removes particles as small as 5 microns.</li><li data-block-key="7bguo">K2 cartridge: reduces particle size to 3 microns.</li><li data-block-key="75erc">Cartridge K7: Provides final filtration down to 0.8 microns (125 times thinner than a human hair).</li></ul><p data-block-key="253fh">The carbon block with AQUALEN ion-exchange fiber reliably traps heavy metals and other hazardous impurities commonly found in tap water.</p><p data-block-key="5m7n7">Instant access to clean water:</p><ul><li data-block-key="dopru">Fills a kettle or pot at a rate of 2.5 liters per minute.</li><li data-block-key="3km60">A glass of clean water in 10 seconds.</li><li data-block-key="f784b">A convenient and affordable filter for preparing food in any quantity, including baby food, soups, and beverages.</li></ul>'
                    }},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content5_img5.png').id,
                        ],
                        'text': '<h3 data-block-key="x25ux"><b>Aquaphor RO-101S</b></h3><p data-block-key="e0sea">An economical and compact reverse osmosis system with a 5-liter clean water supply.</p><p data-block-key="e2jdn">The perfect solution for household water purification!</p><p data-block-key="94rn1">The RO-101S system completely replaces premium bottled water, regardless of the quality of the incoming water. Morion removes all impurities, including toxic substances, bacteria, and viruses, and prevents scale buildup throughout the membrane’s entire service life.</p><p data-block-key="9b64g">Compact and economical:</p><ul><li data-block-key="fe1hu">Takes up half the space under the sink compared to traditional systems with a separate tank.</li><li data-block-key="1s75g">Saves up to 9 tons of water per year.</li><li data-block-key="c8g39">Operates even at low water pressure.</li></ul><p data-block-key="8ghas">High-quality purification:</p><ul><li data-block-key="e3gv5">Significant savings compared to buying bottled water, with guaranteed high-quality purification.</li></ul><p data-block-key="9f8vr">Versatile use:</p><ul><li data-block-key="9ishd">Clean water for drinking, cooking, baby food, and household appliances.</li><li data-block-key="nk70">Complete removal of hardness minerals ensures a long service life for coffee makers, kettles, slow cookers, irons, and steamers.</li><li data-block-key="9c8s4">The humidifier will no longer leave a white residue on your furniture.</li></ul>'
                    }},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content5_img6.png').id,
                        ],
                        'text': '<h3 data-block-key="x25ux">Aquaphor RO-101S</h3><p data-block-key="f2elb">A filter attachment for deep purification of soft water, featuring a filtration mode switch.</p><p data-block-key="f9tmj">The perfect filter for a small family, a compact kitchen, a rental apartment, and travel!</p><p data-block-key="3l8oc">Reliable purification: Effectively removes harmful impurities from the water.</p><p data-block-key="2ohdl">High performance: The highest among filter attachments.</p><p data-block-key="effp6">Convenient to use: No need to disconnect from the faucet to draw unfiltered water—the attachment has a switch.</p><p data-block-key="85dv5">To purify hard water, use special Aquaphor B200 softening cartridges. They effectively remove hardness salts and prevent the formation of scale, white residue, and surface film.</p><p data-block-key="fsu2j">Service life: 4,000 L.</p><p data-block-key="6gc4s">Filtration rate: 1.0–1.2 L/min.</p><p data-block-key="5srvl">Aquaphor Modern—your reliable partner in providing clean water under any conditions!</p>'
                    }},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content5_img7.png').id,
                        ],
                        'text': '<h3 data-block-key="x25ux">Viking for drinking water</h3><p data-block-key="25tt5">The Aquaphor Viking drinking water pre-filter completely removes rust, sand, and insoluble impurities, as well as free chlorine, phenols, heavy metals, and pesticides from the water.</p><p data-block-key="doe33">With just one filter, you’ll get clean water for both the bath and shower, as well as for drinking—right in your kitchen.</p>'
                    }},
                    {"type": "rtfbody", "value": '<h3 data-block-key="x25ux">Glass towel racks</h3><h4 data-block-key="f6n95">ONYX Glass Towel Rack, 2 m, White/Black</h4><p data-block-key="95u50">The ONYX towel rack is designed for those who truly appreciate unique design, uncompromising functionality, and the highest quality.</p>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content5_img8.png').id},
                    {"type": "rtfbody", "value": '<p data-block-key="x25ux">The 2m model is perfectly proportioned. The size and power of this towel warmer also allow it to be used as a heating source for your bathroom.</p><p data-block-key="fa86h">The ONYX towel warmer is not only a stylish piece of interior decor but also a multifunctional device that:</p><ul><li data-block-key="c0kg3">Gently dries towels without overheating them.</li><li data-block-key="24cbj">Heats the bathroom, creating a comfortable temperature.</li><li data-block-key="78f0k">Saves you money thanks to its energy efficiency.</li></ul><p data-block-key="e0443">ONYX Benefits:</p><ul><li data-block-key="2erk7">Gentle drying: Infrared waves evenly dry towels without direct contact with the heating surface, which is ideal for delicate fabrics.</li><li data-block-key="ddos1">Heating: Three heating modes to maintain a comfortable temperature in the bathroom.</li><li data-block-key="d8oa4">Sleep timer: Automatic shut-off after 3 hours to save energy.</li></ul><p data-block-key="8lnl">With the ONYX towel warmer, you’ll always be warm and comfortable, and your towels will stay dry and fresh.</p><p data-block-key="eigee">We also offer towel warmers in smaller and larger sizes to meet all your needs.</p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="x25ux">ONYX Kitchen Black Glass Towel Rack</h3>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content5_img9.png').id},
                    {"type": "rtfbody", "value": '<p data-block-key="elb8e">The ONYX kitchen towel warmer is a unique, patented design from HYBRO that combines stylish design, uncompromising functionality, and the highest quality. It gently dries kitchen towels, warms the kitchen workspace, and saves you money thanks to its energy efficiency. ONYX kitchen features three heating modes and an automatic shut-off timer that activates after 3 hours. Available in three colors: gray, black, and white.</p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="x25ux">Home Heaters</h3><h4 data-block-key="f7etm">Ceramic heating panel</h4><p data-block-key="jfou">The HYBRID panel uses a hybrid heat transfer method that combines two heating principles: infrared and convection. This method allows for maximum heat transfer efficiency in terms of size and power.</p><p data-block-key="9dhu5">The ceramic panel, heated to a temperature of 65–70°C, is an effective heat source operating in the long-wave infrared spectrum of 7–14 microns. A convective heat flow is formed between the wall on which the panel is mounted and the panel itself, the back of which is heated to 80–85°C. The high level of thermal efficiency reduces heating costs by several times compared to traditional heating systems.</p><p data-block-key="4btlt">When heating a room with low-power panels, you can distribute the heat source to avoid excessively cold or hot spots.</p>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content5_img10.png').id},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content5_img11.png').id,
                        ],
                        'text': f"<ul><li data-block-key=\"x25ux\">The 375 panel is part of the HYBRID modular heating system. Depending on the size of the room, you can install one or more panels, allowing for 1 panel per 5–7 m² of floor space. By using the required number of ceramic panels, you can easily heat rooms of any size.</li><li data-block-key=\"6255r\">The panels are also used for supplemental heating. The most popular arrangement is horizontal (in pairs), and the top panel supports additional decorative weight when installed vertically.</li></ul><embed embedtype=\"image\" id=\"{self.get_or_create_seed_image('content5_img12.png').id}\" format=\"left\" alt=\"content5_img12.png\"/>",
                    }},
                    {"type": "rtfbody", "value": '<p data-block-key="v93ns">Also available in other sizes: HYBRID 420 white/black, HYBRID 550 white/black.</p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="v93ns">EGG 2000 Ceramic Heater, Boho / White</h3>'},
                    {"type": "image", "value": self.get_or_create_seed_image('content5_img13.png').id},
                    {"type": "rtfbody", "value": '<p data-block-key="v93ns">EGG is the world’s first all-ceramic heater, impressing with its unique design and efficiency. Thanks to its special shape, it evenly distributes heat in all directions, making it ideal for apartments, homes, and offices. EGG combines infrared and convection heating, ensuring quick and quiet room heating without stirring up dust. The heated ceramic surface, reaching up to 60°C, creates comfortable warmth, while the built-in fan helps heat the room quickly. The heater is made of natural ceramic, ensuring durability and safety. It is controlled via a touch button.</p>'},
                    {"type": "rtfbody", "value": '<h3 data-block-key="v93ns">Electric blankets</h3><p data-block-key="7vru8">The YASAM electric blanket—your trusted companion for warm and cozy nights.</p>'},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content5_img14.png').id,
                        ],
                        'text': '<p data-block-key="v93ns"><b>Why do you need it?</b></p><ul><li data-block-key="8n602">Comfortable warmth: The blanket provides gentle infrared heat that will keep you warm in any position—whether lying down, sitting, or standing.</li><li data-block-key="2lg3n">Versatile use: Ideal for home use, medical facilities, massage parlors, and beauty salons.</li><li data-block-key="3a96s">High-quality materials: Made of polyamide—a quick-drying, durable, and breathable fabric. Inside is an Austrian heating element encased in modern silicone insulation that protects against overheating and damage.</li><li data-block-key="eebp">Easy to care for: The material does not retain moisture or static electricity, is hypoallergenic, and requires no special care.</li><li data-block-key="5m091">Comfortable to use: The sheet retains its shape even after prolonged use, and the seamless surface ensures no discomfort.</li></ul><p data-block-key="3boe6">Adjust the heat to your liking!</p><ul><li data-block-key="59u54">Economy mode: With a power consumption of just 40 W, the sheet heats up to 35°–45°C.Maximum heating: Heats up to 45°–55°C in 25–30 minutes with a power consumption of 80 W.</li><li data-block-key="avbj9">Practicality and convenienceUniversal size: Fits any bed.</li><li data-block-key="abs6s">Compact design: With a thickness of just 7 mm, the sheet is easy to pack for storage or transport.</li></ul><p data-block-key="av625">With the YASAM electric sheet, you’ll always stay warm and comfortable. Try it for yourself and see that cold nights are a thing of the past!</p>'
                    }},
                ]
            },
            {
                # Content page 6
                'title': 'A wide range of furniture',
                'preview_image': self.get_or_create_seed_image('photo_block_1.png'),
                'preview_title': 'A wide range of furniture',
                'preview_description': 'We offer modern, stylish furniture for the home, office and commercial spaces. Choose quality and comfort in every element of your interior.',
                'stream_data': [
                    {"type": "images3oversized", "value": {'images': [
                        self.get_or_create_seed_image('content6_img1.png').id,
                        self.get_or_create_seed_image('content6_img2.png').id,
                        self.get_or_create_seed_image('content6_img3.png').id,
                    ]}},
                    {"type": "rtfbody", "value": '<h2 data-block-key="g7ctb"> A wide selection of furniture</h2>'},
                    {"type": "imagestext", "value": {
                        'layout': 'img-left',
                        'images': [
                            self.get_or_create_seed_image('content6_img4.png').id,
                        ],
                        'text': '<p data-block-key="pubya"><b>Your home is your castle. With Black Red White furniture, it will become even cozier and more elegant.</b></p><p data-block-key="8fi8">We are proud to be the official distributor of Black Red White furniture—a brand synonymous with quality, modern design, and affordability.</p><p data-block-key="dq859">Your home is not just a place where you spend your time. It is your personal universe, a reflection of your style, personality, and taste.</p><p data-block-key="f0k0d">That is why we offer exclusive Black Red White furniture that will transform your space into a cozy haven.</p>'
                    }},
                    {"type": "rtfbody", "value": '<h3 data-block-key="pubya">A selection that will make your heart race:</h3><ul><li data-block-key="5698c"><b>Elegance and functionality:</b> our wardrobes and dressers combine classic beauty with modern technology.</li><li data-block-key="vbrp"><b>Comfort you can feel from the very first touch:</b> plush sofas and armchairs are designed for complete relaxation.</li><li data-block-key="g1vf"><b>Sweet dreams come true:</b> our beds and mattresses offer deep, restful sleep, as if you were floating on a cloud.</li><li data-block-key="e81ka"><b>Culinary masterpieces begin here:</b> our kitchen sets are designed to inspire you to create culinary masterpieces.</li></ul>'},
                    {"type": "images3p2", "value": {'images': [
                        self.get_or_create_seed_image('content6_img5.png').id,
                        self.get_or_create_seed_image('content6_img6.png').id,
                        self.get_or_create_seed_image('content6_img7.png').id,
                        self.get_or_create_seed_image('content6_img8.png').id,
                        self.get_or_create_seed_image('content6_img9.png').id,
                    ]}},
                    {"type": "rtfbody", "value": '<h3 data-block-key="pubya">The advantages of our furniture:</h3><p data-block-key="658g7"></p><ul><li data-block-key="4gum3"><b>Unmatched quality:</b> only proven materials and cutting-edge technology.</li><li data-block-key="9pscd"><b>Glamorous design:</b> our furniture brings global trends right into your home.</li><li data-block-key="38ar0"><b>Prices that delight: </b>we make style affordable without compromising on quality.</li><li data-block-key="bupp7"><b>Furniture with character:</b> every piece reflects your personality and the stories that unfold every day.</li><li data-block-key="3f9q5"><b>A warranty you can trust:</b> we care about you and your comfort, which is why we guarantee the quality of every product.</li></ul><p data-block-key="32o3t">Don’t miss your chance to transform your home with Black Red White furniture!</p><p data-block-key="np5j"></p><p data-block-key="bodl7"> </p><p data-block-key="38u9q">We look forward to seeing you in Alicante, at Plaza Galicia, 1.</p>'},
                ]
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