from django.db import models
from ndarray import NDArrayField
import numpy as np
from autoslug import AutoSlugField
from dj_proposals_candidates.models import Territory, Proposal, Candidate, Commitment


class Propuesta(Proposal):
    position_in_array = models.IntegerField(null=True, blank=True)

class Candidatura(Candidate):
    position_in_array = models.IntegerField(null=True, blank=True)    

class Distrito(Territory):
    matriz = models.BinaryField(null=True, blank=True, default=np.vectorize(np.binary_repr)(np.array([[1, 0, 1], [1, 0, 1]]), width=1))

    def get_matrix(self):
        segunda_dimension = self.candidates.count()
        matrix = np.frombuffer(self.matriz, dtype='<U1').reshape((-1, segunda_dimension)).astype('int_')
        return matrix

class Comuna(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    distrito = models.ForeignKey(Distrito, related_name='comunas', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
