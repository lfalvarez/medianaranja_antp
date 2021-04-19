from django import template
from mn_juego.models import get_percentage, Candidatura

register = template.Library()


@register.filter
def percentage(candidate):
    return get_percentage(candidate)


@register.simple_tag
def get_compromiso_participacion(candidate):
    return candidate.candidatura.get_compromiso_participacion()

@register.simple_tag
def get_compromiso_gep(candidate):
    return candidate.candidatura.get_compromiso_gep()

@register.simple_tag
def se_ha_comprometido(candidate):
    return candidate.candidatura.se_ha_comprometido()