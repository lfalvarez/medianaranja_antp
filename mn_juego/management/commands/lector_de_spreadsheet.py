from __future__ import print_function
from google.oauth2.credentials import Credentials
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '18f-mRM1EB4C0osJjnlgN5t0zYzPvnr74BRWt-NnQaaQ'

nombres_de_las_hojas = [
    'Reporte adherencia',
]

MAPA_DE_COLUMNAS = {
    'Nombre': 'name',
    'Nombre Candidatura Oficial': 'name',
    'Pueblo': 'distrito',
    'Distrito': 'distrito',
    'IG': 'instagram',
    'Facebook': 'facebook',
    '¿Qué compromiso firmó?': 'compromisos'
}

columnas_que_importan = ['Nombre',
                         'Nombre Candidatura Oficial',
                         'Distrito',
                         'Pueblo',
                         'IG',
                         'Facebook',
                         '¿Qué compromiso firmó?']

NOMBRE_COLUMNAS = '{hoja}!1:1'


def get_letra_columna(number):
    return chr(number + 65)


def get_columnas_importantes(columnas):
    result = {}
    for indice, nombre_columna in enumerate(columnas):
        if nombre_columna in columnas_que_importan:
            result[nombre_columna] = indice
    return result


class Lector:
    def __init__(self):
        service = build('sheets', 'v4', credentials=self.get_creds())
        sheet = service.spreadsheets()
        self.sheet = sheet

    def get_creds(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        return creds

    def obtener_candidaturas_y_datos(self, hoja, columnas_importantes):
        result = []

        range_name = '{hoja}!1:1000'.format(hoja=hoja)
        los_datos = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=range_name).execute()
        los_datos = los_datos['values']
        for numero_fila, contenido in enumerate(los_datos):
            if not numero_fila:
                continue
            datos_candidatura = {}
            for nombre_col, num_col in columnas_importantes.items():
                nombre_contenido = MAPA_DE_COLUMNAS[nombre_col]
                try:
                    el_dato = contenido[num_col]
                except:
                    el_dato = None
                datos_candidatura[nombre_contenido] = el_dato
            result.append(datos_candidatura)
        return result

    def ejecutar(self):
        datos_finales = []
        for hoja in nombres_de_las_hojas:
            columnas_range = NOMBRE_COLUMNAS.format(hoja=hoja)
            result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                             range=columnas_range).execute()
            columnas = result['values'][0]
            columnas_importantes = get_columnas_importantes(columnas)
            candidaturas_comprometidas_e_rrss = self.obtener_candidaturas_y_datos(hoja,
                                                                                  columnas_importantes)
            datos_finales += candidaturas_comprometidas_e_rrss
        return datos_finales
