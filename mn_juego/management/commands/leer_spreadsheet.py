from __future__ import print_function
from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned
from mn_juego.management.commands.lector_de_spreadsheet import Lector
from dj_proposals_candidates.models import Commitment
from mn_juego.models import Distrito, Propuesta
import json
from django.conf import settings


class Command(BaseCommand):
    help = 'leer el spreadsheet y ver qué onda'

    def __init__(self):
        super()
        self.p_gep = Propuesta.objects.get(remote_id=settings.PARTICIPACION_PROPOSAL_REMOTE_ID)
        self.p_participacion = Propuesta.objects.get(remote_id=settings.GEP_PROPOSAL_REMOTE_ID)

    def handle(self, *args, **options):

        lector = Lector()
        datos = lector.ejecutar()
        candidatos_comprometidos = []
        for d in datos:
            if d['compromisos']:
               candidatos_comprometidos.append(d)
        with open('data.json', 'w') as outfile:
            json.dump(candidatos_comprometidos, outfile)
        for dato_candidato in candidatos_comprometidos:
            numero_distrito = [int(i) for i in dato_candidato['distrito'].split() if i.isdigit()]
            if numero_distrito:
                numero_distrito = numero_distrito[0]
                nombre_distrito = 'Distrito {numero}'.format(numero=numero_distrito)
                distrito = Distrito.objects.get(name=nombre_distrito)
                nombre_candidato = dato_candidato['name']
                nombre_candidato = nombre_candidato.split("(")[0].strip()
                try:
                    candidate = distrito.candidates.get(name__icontains=nombre_candidato)
                except MultipleObjectsReturned:
                    print('La candidatura de {candidate} en {distrito} está repetido'.format(candidate=nombre_candidato,
                                                                                           distrito=nombre_distrito))
                except:
                    print('No pillé a {candidate} del {distrito}'.format(candidate=nombre_candidato,
                                                                         distrito=nombre_distrito))
                    continue
                self.set_compromisos(candidate, dato_candidato)

    def set_compromisos(self, candidate, dato_candidato):
        compromisos = dato_candidato['compromisos']
        comprometer_gep = False
        debo_crear_participacion = False
        if compromisos.strip() == 'ambos':
            debo_crear_participacion = True
            comprometer_gep = True
        if compromisos.strip() == 'GEP':
            comprometer_gep = True
        if compromisos.strip() == 'Participación':
            debo_crear_participacion = True
        if comprometer_gep:
            ya_comprometido = Commitment.objects.filter(candidate=candidate, proposal=self.p_gep).exists()
            if not ya_comprometido:
                Commitment.objects.create(candidate=candidate, proposal=self.p_gep)
                print('Creado compromiso entre {candidate} y la propuesta por la inclusión'.format(candidate=candidate.name))
        if debo_crear_participacion:
            ya_comprometido = Commitment.objects.filter(candidate=candidate, proposal=self.p_participacion).exists()

            if not ya_comprometido:
                Commitment.objects.create(candidate=candidate, proposal=self.p_participacion)
                print('Creado compromiso entre {candidate} y la propuesta por la participación'.format(candidate=candidate.name))
        if dato_candidato['instagram']:
            candidate.instagram = dato_candidato['instagram']
        if dato_candidato['facebook']:
            candidate.facebook = dato_candidato['facebook']
        candidate.save()











