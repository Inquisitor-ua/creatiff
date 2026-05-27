from django import template
from main.forms import ContactForm
from main.snippets import HeaderSettings, FooterSettings

register = template.Library()

@register.inclusion_tag('main/components/contact_form.html')
def contact_form():
    return {'form': ContactForm()}

@register.inclusion_tag('main/components/header.html', takes_context=True)
def header(context):
    header_settings = HeaderSettings.objects.first()
    context.update({
        'header_settings': header_settings,
    })
    return context

@register.inclusion_tag('main/components/footer.html', takes_context=True)
def footer(context):
    footer_settings = FooterSettings.objects.first()
    context.update({
        'footer_settings': footer_settings,
    })
    return context

