from django.db import models
from autoslug import AutoSlugField
from dj_proposals_candidates.models import Territory, Proposal, Candidate, Commitment
import random
from django.conf import settings


def get_percentage(candidate):
    total = 2
    total += candidate.territory.proposals.count()
    commited = candidate.territory.proposals.filter(commitments__candidate=candidate).count()
    if total:
        return (commited / total) * 100
    return 0


class Propuesta(Proposal):
    position_in_array = models.IntegerField(null=True, blank=True)


class InstitucionPoliticaBase(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')


    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Lista(InstitucionPoliticaBase):
    pass

class Partido(InstitucionPoliticaBase):
    lista = models.ForeignKey(Lista, related_name='partidos', on_delete=models.CASCADE)


class Candidatura(Candidate):
    position_in_array = models.IntegerField(null=True, blank=True)
    partido = models.ForeignKey(Partido,
                                related_name='candidaturas',
                                on_delete=models.CASCADE,
                                null=True)
    facebook = models.URLField(default=None, null=True, blank=True)
    instagram = models.URLField(default=None, null=True, blank=True)

    def get_compromiso_participacion(self):
        return self.commitments.\
            filter(proposal__remote_id=settings.PARTICIPACION_PROPOSAL_REMOTE_ID).exists()

    def get_compromiso_gep(self):
        return self.commitments.\
            filter(proposal__remote_id=settings.GEP_PROPOSAL_REMOTE_ID).exists()

    def se_ha_comprometido(self):
        return any([self.get_compromiso_gep(),
                    self.get_compromiso_participacion()])

class GetSortedCandidatesMixin():
    def get_sorted_candidates(self):
        return sorted(self.candidates.all(), key=get_percentage, reverse=True)


class RegionTerritory(Territory):
    link_geo_referencia = models.URLField(max_length=1024)


class Distrito(Territory, GetSortedCandidatesMixin):
    region_territory = models.ForeignKey(RegionTerritory, related_name='distritos_territory', on_delete=models.CASCADE, null=True)
    link_compromiso_inclusion = models.URLField(default='https://ahoranostocaparticipar.cl/processes/espaciocompromisos/f/128/proposals/8')
    link_compromiso_participacion = models.URLField(default='https://ahoranostocaparticipar.cl/processes/espaciocompromisos/f/128/proposals/7')

    def esta_vacio_de_compromisos(self):
        return not Commitment.objects.filter(candidate__in=self.candidates.all()).exists()


class PuebloOriginario(Territory, GetSortedCandidatesMixin):
    regiones = models.ManyToManyField(Territory,
                                      related_name='pueblos_originarios')


class Comuna(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    distrito = models.ForeignKey(Distrito, related_name='comunas', on_delete=models.CASCADE)
    participacion = models.FloatField(default=0)

    def __str__(self):
        return self.name
