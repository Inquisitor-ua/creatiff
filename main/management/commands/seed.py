from django.core.management.base import BaseCommand
from django.utils.text import slugify
from wagtail.models import Page, Site
from main.models import HomePage, ContentPage 


class Command(BaseCommand):
    help = "Automatically creates a homepage, default site setup, and populates content pages."

    def handle(self, *args, **options):
        # ----------------------------------------------------
        # 1. Создание или получение HomePage
        # ----------------------------------------------------
        root_page = Page.objects.get(id=1)

        if not HomePage.objects.exists():
            homepage = HomePage(
                title="Homepage",
                slug="homepage",
                live=True,
            )
            root_page.add_child(instance=homepage)
            self.stdout.write(self.style.SUCCESS("Successfully created HomePage."))
        else:
            homepage = HomePage.objects.first()
            self.stdout.write("HomePage already exists.")

        # ----------------------------------------------------
        # 2. Привязка к дефолтному сайту
        # ----------------------------------------------------
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            if site.root_page != homepage:
                site.root_page = homepage
                site.save()
        else:
            Site.objects.create(
                hostname="localhost",
                port=8000,
                root_page=homepage,
                is_default_site=True,
            )

        # Удаляем стандартную заглушку Wagtail, если она есть
        Page.objects.filter(slug="home").delete()

        # ----------------------------------------------------
        # 3. Автозаполнение ContentPage
        # ----------------------------------------------------
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

            # Проверяем, не была ли страница создана ранее (чтобы seed можно было запускать повторно)
            if not ContentPage.objects.filter(slug=generated_slug).exists():
                new_page = ContentPage(
                    title=page['title'],
                    slug=generated_slug,
                    preview_title=page['preview_title'],
                    preview_description=page['preview_description'],
                    body=page['stream_data'], # Передаем чистый список, т.к. реальная модель сама все обработает
                )
                
                # Добавляем в дерево к найденному/созданному homepage
                homepage.add_child(instance=new_page)
                
                # Создаем ревизию и публикуем, чтобы страница стала "Live"
                new_page.save_revision().publish()
                
