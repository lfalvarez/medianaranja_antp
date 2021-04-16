from django.core.management.base import BaseCommand, CommandError
from mn_juego.models import Distrito, Comuna, Territory
import csv
import re


def get_number_from_string(string):
    pattern = re.compile('(?P<number>\d+)')
    match = pattern.search(string)
    return match.group('number')


class Command(BaseCommand):
    help = 'carga distritos y comunas'

    def __init__(self):
        super()
        self.pais, created = Territory.objects.get_or_create(name="Chile", remote_id=1, is_country=True)

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **options):
        for filename in options['filename']:
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                lines = [line for line in csv_reader]
                self.process_csv(lines)

    def process_csv(self, lines):
        for line in lines:
            self.process_one_line(line)

    def process_one_line(self, line):
        (region_name, distrito_name, comuna_name) = self.get_region_distrito_comuna(line)
        region, created = Territory.objects.get_or_create(name=region_name, remote_id=1)
        distrito, d_created = Distrito.objects.get_or_create(name=distrito_name,
                                                             region=region,
                                                             remote_id=get_number_from_string(distrito_name))
        comuna, c_created = Comuna.objects.get_or_create(name=comuna_name, distrito=distrito)

    def get_region_distrito_comuna(self, line):
        region = line[0]
        region = region.replace('\n', ' ')
        distrito = line[1]
        distrito = 'Distrito {numero}'.format(numero=distrito)
        comuna = line[2]
        return (region, distrito, comuna)
