from django import template
from main.forms import ContactForm
from main.snippets import ContactFormSettings, HeaderSettings, FooterSettings

register = template.Library()

@register.inclusion_tag('main/components/contact_form.html', takes_context=True)
def contact_form(context):
    page = context.get('page')
    contact_form_settings = None

    if page and hasattr(page, 'contact_form_settings'):
        contact_form_settings = page.contact_form_settings

    if not contact_form_settings:
        contact_form_settings = ContactFormSettings.objects.filter(locale=page.locale).first()

    form = ContactForm(settings=contact_form_settings)
    return {
        'form': form,
        'contact_form_settings': contact_form_settings,
    }

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

@register.inclusion_tag('main/components/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    page = context.get('page')
    ancestors = []
    if page:
        ancestors = page.get_ancestors().live().exclude(depth=1)

    context.update({
        'ancestors': ancestors,
        'current_page': page,
    })
    return context