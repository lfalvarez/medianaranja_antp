from django.core.management.base import BaseCommand, CommandError
from mn_juego.models import Distrito, Comuna, Territory, Candidatura, Lista, Partido
import csv
import re


def get_number_from_string(string):
    pattern = re.compile('(?P<number>\d+)')
    match = pattern.search(string)
    return match.group('number')

class Command(BaseCommand):
    help = 'carga candidaturas a distritos'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **options):
        for filename in options['filename']:
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                lines = [line for line in csv_reader]
                self.process_csv(lines)

    def process_csv(self, lines):
        headers = lines.pop(0)
        for line in lines:
            self.process_one_line(line)

    def process_one_line(self, line):
        elements = self.get_things(line)
        if not elements:
            return
        (distrito_name, candidate_name, lista_name, partido_name, mail) = elements
        if lista_name and partido_name:
            lista, l_created = Lista.objects.get_or_create(name=lista_name)
            partido, p_created = Partido.objects.get_or_create(name=partido_name, lista=lista)
        else:
            partido = None
        distrito = Distrito.objects.get(name=distrito_name)
        candidate, c_created = Candidatura.objects.get_or_create(name=candidate_name,
                                                                 territory=distrito)
        if partido:
            candidate.partido = partido
            candidate.save()

    def get_things(self, line):
        try:
            distrito_name = get_number_from_string(line[1])
        except Exception as e:
            print(e, line)
            return
        distrito_name = 'Distrito {numero}'.format(numero=distrito_name)
        candidate_name = line[2]
        lista = line[3]
        partido = line[4]
        mail = line[5]
        return (distrito_name, candidate_name, lista, partido, mail)