from django import template
from main.forms import ContactForm

register = template.Library()

@register.inclusion_tag('main/ContactForm.html')
def contact_form():
    return {'form': ContactForm()}

@register.inclusion_tag('main/Footer.html')
def footer():
    return {}