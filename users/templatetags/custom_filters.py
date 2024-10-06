import datetime
from django import template

register = template.Library()

@register.filter
def parse_datetime(value):
    if isinstance(value, datetime.datetime):
        return value
    try:
        return datetime.datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return value