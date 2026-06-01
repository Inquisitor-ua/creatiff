from django.db import migrations


def create_default_header_footer(apps, schema_editor):
    HeaderSnippet = apps.get_model('main', 'HeaderSettings')
    FooterSnippet = apps.get_model('main', 'FooterSettings')

    FooterSnippet.objects.get_or_create(
        caption = 'Feedback',
        rights = '© 2024 Star Creatiff. Todos los derechos reservados.'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_footersettings_headersettings_homepage_body_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_header_footer),
    ]