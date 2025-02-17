from django import template
from dateutil import parser

register = template.Library()

@register.filter
def iso_to_datetime(value):
    try:
        return parser.parse(value)
    except Exception:
        return value