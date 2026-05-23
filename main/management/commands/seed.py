from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from main.models import HomePage  # Замени на твою модель


class Command(BaseCommand):
    help = "Automatically creates a homepage and sets it as the root page for the default site."

    def handle(self, *args, **options):
        # 1. Get the root page (the default Wagtail root page has id=1)
        root_page = Page.objects.get(id=1)

        # 2. If the homepage doesn't exist, create it as a child of the root page
        if not HomePage.objects.exists():
            homepage = HomePage(
                title="Homepage",
                slug="homepage",
                live=True,
            )
            # At this moment the search tables are already in place, everything will work as expected
            root_page.add_child(instance=homepage)
        else:
            homepage = HomePage.objects.first()

        # 3. Bind it to the default site
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

        # 4. Remove the default Wagtail placeholder page if it exists
        Page.objects.filter(slug="home", depth=3).delete()