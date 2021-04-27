from __future__ import print_function
from django.core.management.base import BaseCommand

from mn_juego.management.commands.lector_de_spreadsheet import Lector
from mn_juego.models import Distrito
import json


class Command(BaseCommand):
    help = 'leer el spreadsheet y ver qué onda'

    def handle(self, *args, **options):
        lector = Lector()
        datos = lector.ejecutar()
        para_imprimir = []
        for d in datos:
            if d['compromisos']:
               para_imprimir.append(d)
        with open('data.json', 'w') as outfile:
            json.dump(para_imprimir, outfile)
        #for dato_candidato in datos:
        #    distrito_num = dato_candidato['distrito']
        #    if distrito_num.isnumeric():
        #        distrito = Distrito.objects.get('Distrito {numero}'.format(numero=distrito_num))
        #        print(distrito)










