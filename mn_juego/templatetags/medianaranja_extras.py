from django import template
from mn_juego.models import get_percentage, Candidatura, Comuna, PuebloOriginario

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

@register.simple_tag
def esta_vacio_de_compromisos(distrito):
    return distrito.esta_vacio_de_compromisos()

@register.inclusion_tag('componentes/buscador_comunas.html')
def buscador_comunas(input_id, pre_fix):
    object_list = Comuna.objects.all()
    return {'object_list': object_list, 'input_id': input_id, 'pre_fix': pre_fix}

@register.inclusion_tag('componentes/buscador_comunas.html')
def buscador_pueblos_originarios(input_id, pre_fix):
    object_list = PuebloOriginario.objects.all()
    return {'object_list': object_list, 'input_id': input_id, 'pre_fix': pre_fix}
