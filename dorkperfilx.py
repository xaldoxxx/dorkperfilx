# !/usr/bin/env python
# Buscar perfiles públicos según correo...
# Uso: #!python dorkperfilx.py --email manfredialdo789@gmail.com
import sys
import logging
import argparse
import requests
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
logger = logging.getLogger('buscador_perfiles')
logger.setLevel(logging.INFO)

MOTOR_DE_BUSQUEDA = "https://www.google.com/search?q="

def buscar_correo(correo):
    """
    Realiza una búsqueda en Google para obtener posibles perfiles de redes sociales o datos públicos del correo.
    """
    consulta = f"{correo} LinkedIn OR GitHub OR Twitter OR Facebook OR profile"
    encabezados = {"User-Agent": "Mozilla/5.0"}

    try:
        respuesta = requests.get(MOTOR_DE_BUSQUEDA + consulta, headers=encabezados)
        respuesta.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error al realizar la búsqueda: {e}")
        return None

    sopa = BeautifulSoup(respuesta.text, 'html.parser')
    resultados = []
    for item in sopa.find_all('a', href=True):
        enlace = item['href']
        if "url?q=" in enlace and not enlace.startswith("/search"):
            enlace_real = enlace.split("url?q=")[1].split("&")[0]
            if any(red_social in enlace_real for red_social in ["linkedin", "github", "twitter", "facebook"]):
                resultados.append(enlace_real)
    return resultados

def formatear_resultados(resultados):
    """
    Formatea los resultados de búsqueda en una cadena de texto.
    """
    resumen = "Perfiles encontrados:\n"
    for resultado in resultados:
        resumen += f"- {resultado}\n"
    return resumen if resultados else "No se encontraron perfiles.\n"

def procesar_correo(correo, archivo_salida=None):
    """
    Procesa un solo correo electrónico para buscar perfiles públicos.
    """
    resultados = buscar_correo(correo)
    if resultados:
        logger.info(f"Perfiles públicos encontrados para {correo}")
        resumen = formatear_resultados(resultados)
        print(resumen)
        if archivo_salida:
            archivo_salida.write(resumen + '\n')
    else:
        print(f"No se encontró información para {correo}\n")

def main():
    """
    Lee una lista de correos electrónicos e intenta buscar perfiles públicos para cada uno.
    """
    parser = argparse.ArgumentParser(description='Busca perfiles públicos usando un motor de búsqueda')
    parser.add_argument('--salida', '-s', type=argparse.FileType('w'), help='Archivo de salida para los resultados')
    parser.add_argument('--correo', '-c', help='Dirección de correo electrónico para consultar')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.correo:
        procesar_correo(args.correo, args.salida)
    else:
        for linea in sys.stdin:
            procesar_correo(linea.strip(), args.salida)

if __name__ == '__main__':
    main()

# !python dorkxperfilx.py --correo alearcar@hotmail.com
'''
Instrucciones de uso:
Ejecuta con un correo específico: python dorkperfilx.py --correo ejemplo@ejemplo.com
Para procesar una lista de correos: cat correos.txt | python dorkperfilx.py --salida resultados.txt
'''
