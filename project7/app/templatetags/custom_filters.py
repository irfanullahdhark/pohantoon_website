from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import strip_tags


register = template.Library()

@register.filter(name='truncate_html')
@stringfilter
def truncate_html(value,arg):
    length = int(arg)
    value = value.replace('&nbsp;', ' ')
    value = value.replace('&ndash;', '-')

    truncated_text = strip_tags(value)[:length]
    return truncated_text