from __future__ import print_function
from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned
from mn_juego.management.commands.lector_de_spreadsheet import Lector
from dj_proposals_candidates.models import Commitment
from mn_juego.models import Distrito, Propuesta
import json
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'leer el spreadsheet y ver qué onda'

    def __init__(self):
        super()
        self.p_gep = Propuesta.objects.get(remote_id=settings.GEP_PROPOSAL_REMOTE_ID)
        self.p_participacion = Propuesta.objects.get(remote_id=settings.PARTICIPACION_PROPOSAL_REMOTE_ID)

    def handle(self, *args, **options):

        lector = Lector()
        datos = lector.ejecutar()
        candidatos_comprometidos = []
        for d in datos:
            if d['compromisos']:
               candidatos_comprometidos.append(d)
        with open('data.json', 'w') as outfile:
            json.dump(candidatos_comprometidos, outfile)
        resultado = ''
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
                    resultado += 'La candidatura de {candidate} en {distrito} está repetido\n'.format(candidate=nombre_candidato,
                                                                                           distrito=nombre_distrito)
                except:
                    resultado += 'No pillé a {candidate} del {distrito}\n'.format(candidate=nombre_candidato,
                                                                         distrito=nombre_distrito)
                    continue
                resultado += self.set_compromisos(candidate, dato_candidato)

        self.enviar_mail(resultado)

    def set_compromisos(self, candidate, dato_candidato):
        str_resultado = ''
        compromisos = dato_candidato['compromisos']
        comprometer_gep = False
        debo_crear_participacion = False
        if compromisos.lower().strip() == 'ambos':
            debo_crear_participacion = True
            comprometer_gep = True
        if compromisos.lower().strip() == 'gep':
            comprometer_gep = True
        if compromisos.lower().strip() == 'participación':
            debo_crear_participacion = True
        if comprometer_gep:
            ya_comprometido = Commitment.objects.filter(candidate=candidate, proposal=self.p_gep).exists()
            if not ya_comprometido:
                Commitment.objects.create(candidate=candidate, proposal=self.p_gep)
                str_resultado += 'Creado compromiso entre {candidate} y la propuesta por la inclusión\n'.format(candidate=candidate.name)
        if debo_crear_participacion:
            ya_comprometido = Commitment.objects.filter(candidate=candidate, proposal=self.p_participacion).exists()

            if not ya_comprometido:
                Commitment.objects.create(candidate=candidate, proposal=self.p_participacion)
                str_resultado += 'Creado compromiso entre {candidate} y la propuesta por la participación\n'.format(candidate=candidate.name)
        if dato_candidato['instagram']:
            candidate.instagram = dato_candidato['instagram']
        if dato_candidato['facebook']:
            candidate.facebook = dato_candidato['facebook']
        candidate.save()
        return str_resultado

    def enviar_mail(self, resultado):
        if resultado:
            mensaje_formateado = 'hola!\n' \
                                 'Este es un mail automático que' \
                                 'quiere contarte cuál fue el resultado del último procesamiento del spreadsheet\n\n' \
                                 '{resultado}' \
                                 '\n\n\n' \
                                 'Besos y abrazos\n' \
                                 '--\n' \
                                 'La máquina'.format(resultado=resultado)
            send_mail(
                'Resultado ',
                mensaje_formateado,
                settings.DEFAULT_FROM_EMAIL,
                [m.strip() for m in settings.A_QUIEN_SE_LE_VA_ELMAIL.split(',')],
                fail_silently=False,
            )











