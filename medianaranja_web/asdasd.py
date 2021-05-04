from dj_proposals_candidates.models import Territory

from mn_juego.models import RegionTerritory

t_names = ["Arica y Parinacota",
"Tarapacá",
"Antofagasta",
"Atacama",
"Coquimbo",
"Valparaíso",
"Metropolitana de Santiago",
"O'Higgins",
"Maule",
"Ñuble",
"Biobío",
"Araucanía",
"Los Ríos",
"Los Lagos",
"Aysén",
"Magallanes y la Antártica Chilena"]

for t in Territory.objects.filter(name__in=t_names):
    r = RegionTerritory.objects.create(territory_ptr_id=t.id, remote_id=t.id, name=t.name)
