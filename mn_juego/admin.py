from django.contrib import admin

from dj_proposals_candidates.models import Commitment
from mn_juego.models import (
    Propuesta,
    Candidatura,
    RegionTerritory
)

class CommitmentInline(admin.TabularInline):
    model = Commitment

@admin.register(Propuesta)
class PropuestaAdmin(admin.ModelAdmin):
    inlines = [CommitmentInline, ]

@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ('name', 'territory')
    search_fields = ('name',)


@admin.register(RegionTerritory)
class RegionTerritoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_geo_referencia')
