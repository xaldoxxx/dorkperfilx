# controlador.py

import logging
from modelo import buscar_correo, formatear_resultados

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.vista.buscar_perfiles = self.buscar_perfiles

    def buscar_perfiles(self):
        """
        Controla la búsqueda de perfiles y la visualización de resultados en la interfaz.
        """
        correo, verbose, archivo_salida = self.vista.obtener_datos()
        
        if verbose:
            logging.getLogger('buscador_perfiles').setLevel(logging.DEBUG)
        else:
            logging.getLogger('buscador_perfiles').setLevel(logging.INFO)
        
        if not correo:
            self.vista.mostrar_resultados("Por favor, ingrese una dirección de correo electrónico.")
            return

        # Buscar perfiles usando el modelo
        resultados = buscar_correo(correo)
        if resultados:
            resumen = formatear_resultados(resultados)
            self.vista.mostrar_resultados(resumen)

            # Guardar en archivo si se ha especificado
            if archivo_salida:
                with open(archivo_salida, 'w') as archivo:
                    archivo.write(resumen)
        else:
            self.vista.mostrar_resultados("No se encontraron perfiles para el correo proporcionado.")
