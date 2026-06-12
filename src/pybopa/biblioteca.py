import json
from datetime import datetime, timedelta
from .boletin import Boletin

import json
from datetime import datetime
from .boletin import Boletin


class Biblioteca:
    """
    Clase para gestionar una colección de boletines y sus disposiciones.

    Atributos
    ----------
    boletines : list
        Lista de objetos Boletin.
    """

    def __init__(self):
        """
        Inicializa la clase Biblioteca con una lista vacía de boletines.
        """
        self.boletines = []

    def agregar_boletin(self, boletin):
        """
        Agrega un boletín a la lista de boletines.

        Parameters
        ----------
        boletin : Boletin
            El objeto Boletin a agregar a la biblioteca.
        """
        self.boletines.append(boletin)

    def obtener_disposiciones(self, desde, hasta, archivo_json=None):
        """
        Obtiene todas las disposiciones de los boletines en un rango de fechas y las guarda en un archivo JSON.

        Parameters
        ----------
        desde : str
            La fecha de inicio del rango en formato dd/mm/yyyy.
        hasta : str
            La fecha de fin del rango en formato dd/mm/yyyy.

        Returns
        -------
        None
        """
        boletines = []
        # Recorrer los boletines de las fechas indicadas
        fecha_desde = datetime.strptime(desde, "%d/%m/%Y")
        fecha_hasta = datetime.strptime(hasta, "%d/%m/%Y")
        fecha_actual = fecha_desde
        while fecha_actual <= fecha_hasta:
            fecha_str = fecha_actual.strftime("%d/%m/%Y")

            try:
                nuevo_boletin = Boletin(fecha=fecha_str)
                nuevo_boletin._get_disposiciones()
                boletines.append(nuevo_boletin)
            except Exception as e:
                with open('error.log', 'a') as file:
                    file.write(f"Error al crear el boletin del día {
                                fecha_str}: {str(e)}\n")

            fecha_actual += timedelta(days=1)

        disposiciones = []
        for boletin in boletines:
            print(boletin.disposiciones)
            for disp in boletin.disposiciones:
                disposiciones.append(disp)

        disposiciones_json = [json.loads(str(disposicion))
                                for disposicion in disposiciones]
        json_concatenado = json.dumps(
            disposiciones_json, ensure_ascii=False, indent=4)

        # Si se indica el nombre de un archivo se crea con ese nombre
        if archivo_json:
            nombre_archivo = archivo_json if isinstance(archivo_json, str) else False
            if not nombre_archivo:
                nombre_archivo = f"texto_disposiciones_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.json"
            with open(nombre_archivo, 'w', encoding='utf-8') as file:
                file.write(json_concatenado)
                # print(f"JSON con el texto de las disposiciones guardado en {nombre_archivo}")
