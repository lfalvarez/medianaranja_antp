from django.db import models
from autoslug import AutoSlugField
from dj_proposals_candidates.models import Territory, Proposal, Candidate, Commitment


def get_percentage(candidate):
    total = candidate.territory.proposals.count()
    commited = candidate.territory.proposals.filter(commitments__candidate=candidate).count()
    if total:
        return (commited / total) * 100
    return 0


class Propuesta(Proposal):
    position_in_array = models.IntegerField(null=True, blank=True)

class Candidatura(Candidate):
    position_in_array = models.IntegerField(null=True, blank=True)
    importante_para_antp = models.BooleanField(default=False)

class GetSortedCandidatesMixin():
    def get_sorted_candidates(self):
        return sorted(self.candidates.all(), key=get_percentage, reverse=True)

class Distrito(Territory, GetSortedCandidatesMixin):
    region = models.ForeignKey(Territory, related_name='distritos', on_delete=models.CASCADE)


class PuebloOriginario(Territory, GetSortedCandidatesMixin):
    regiones = models.ManyToManyField(Territory,
                                      related_name='pueblos_originarios')


class Comuna(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    distrito = models.ForeignKey(Distrito, related_name='comunas', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
