from django import template
from mn_juego.models import get_percentage

register = template.Library()


@register.filter
def percentage(candidate):
    return get_percentage(candidate)
