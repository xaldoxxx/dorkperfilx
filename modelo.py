# modelo.py

import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M')
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
