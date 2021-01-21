import numpy as np
from mn_juego.models import Propuesta, Candidatura



class CandidateResult:
    def __init__(self, candidate, porcentaje):
        self.candidate = candidate
        self.porcentaje = porcentaje

    def __str__(self):
        return '{candidate} con {porcentaje}%'.format(candidate=self.candidate.name, porcentaje=self.porcentaje * 100)


class ResultsGame:
    def __init__(self, distrito):
        self.distrito = distrito
        self.matrix = distrito.get_matrix()

    def calculate_result(self, chosen_proposals):
        propuestas = Propuesta.objects.filter(territory=self.distrito, id__in=[p.id for p in chosen_proposals])
        propuestas_count = propuestas.count()
        vector = np.zeros(self.distrito.proposals.count())
        for propuesta in propuestas:
            vector[propuesta.position_in_array] = 1
        results = np.dot(np.transpose(self.matrix), vector)
        results_and_candidates = []
        position = 0
        for r in results:
            candidate = Candidatura.objects.get(position_in_array=position)
            results_and_candidates.append((r, candidate))
            position += 1
        resultados_ordenado = sorted(results_and_candidates, key=lambda x: -x[0])
        resultados_con_candidato = []
        for resultado in resultados_ordenado:
            r = CandidateResult(resultado[1], resultado[0]/propuestas_count)
            resultados_con_candidato.append(r)
        return resultados_con_candidato

                                                                                                                                         