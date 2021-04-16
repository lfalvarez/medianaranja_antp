from django.core.management.base import BaseCommand, CommandError
from mn_juego.models import Distrito, Comuna, Territory, Candidatura, PuebloOriginario
import csv
import re


def get_number_from_string(string):
    pattern = re.compile('(?P<number>\d+)')
    match = pattern.search(string)
    return match.group('number')

class Command(BaseCommand):
    help = 'carga candidaturas de pueblos originarios'

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
        (pueblo, candidate_name, region, mail) = elements
        region = Territory.objects.get(name=region)
        distrito, d_created = PuebloOriginario.objects.get_or_create(name=pueblo, remote_id=2)
        distrito.regiones.add(region)
        candidate, c_created = Candidatura.objects.get_or_create(name=candidate_name, territory=distrito)
        print(candidate)

    def get_things(self, line):
        pueblo = line[1]
        candidate_name = line[0]
        region = line[2]
        mail = line[3]
        return (pueblo, candidate_name, region, mail)