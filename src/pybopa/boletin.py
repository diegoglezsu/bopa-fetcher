import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from .disposicion import Disposicion


class Boletin:
    """
    Clase para representar un Boletín Oficial del Principado de Asturias (BOPA).

    Atributos
    ----------
    num : str, opcional
        El número del boletín (por defecto es None). 
    fecha : datetime
        La fecha del boletín.
    cods : list
        Una lista de los códigos de las disposiciones del boletín.
    sumario : dict
        El contenido parseado del sumario del boletín.
    disposiciones : list
        Una lista de objetos Disposicion que representan las disposiciones del boletín.
    """

    def __init__(self, fecha=None):
        """
        Construye todos los atributos necesarios para el objeto Boletin.

        Parámetros
        ----------
        fecha : str, opcional
            La fecha del boletín (por defecto es None).
        """

        if fecha is None:
            self.fecha = datetime.now()
        else:
            try:
                # Process the date as a string
                self.fecha = datetime.strptime(fecha, "%d/%m/%Y")
            except ValueError:
                raise ValueError(
                    "El formato de la fecha no es válido. Por favor, proporciona una fecha con formato dd/mm/yyyy.")

        self.cods = []
        self.sumario = self._get_sumario()
        self.disposiciones = []

    def _get_boletin(self):
        """
        Obtiene el contenido HTML del boletín desde la URL especificada.

        Devuelve
        ---------
        bs4.element.Tag
            El div que contiene el boletín si se encuentra, de lo contrario se lanza una excepción.

        Raises
        ------
        Exception
            Si no se encuentra el div con id='bopa-boletin'.
        """

        # Formatear la URL sobre la que se hace la consulta con la fecha
        day = self.fecha.strftime("%d")
        month = self.fecha.strftime("%m")
        year = self.fecha.strftime("%Y")
        url = f"https://sede.asturias.es/ultimos-boletines?p_r_p_summaryDate={
            day}%2F{month}%2F{year}"

        # Obtener el contenido HTML de la página
        response = requests.get(url, timeout=60)
        html_content = response.content

        # Parsear el HTML usando BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Buscar el elemento h3 con la clase "tit-redon-azul"
        h3_element = soup.find('h3', class_='tit-redon-azul')

        # Extraer el texto dentro del span
        span_text = h3_element.find('span').get_text(strip=True)

        # Buscar el número de boletín en el texto
        match = re.search(r'Boletín Nº (\d+)', span_text)
        if match:
            self.num = match.group(1)

        # Encontrar el elemento div con id="bopa-boletin"
        boletin_div = soup.find("div", {"id": "bopa-boletin"})

        if boletin_div:
            return boletin_div
        else:
            raise Exception("No se encontró el div con id='bopa-boletin'.")

    def _get_sumario(self):
        """
        Parsear el contenido del boletín y devolverlo como un diccionario estructurado.

        Devuelve
        ---------
        dict
            Un diccionario que contiene el contenido estructurado del boletín.
        """

        # Esto devolverá una exception si no puede obtener el boletín
        boletin_div = self._get_boletin()

        # Inicializar un diccionario vacío para almacenar los encabezados
        headers_dict = {}

        # Inicializar variables para rastrear los h4, h5 y h6
        current_h4 = None
        current_h5 = None
        current_h6 = None
        current_subauthor = None

        # Recorrer todos los elementos dentro de boletin_div
        for element in boletin_div.children:

            if element.name == 'h4':
                current_h4 = element.get_text().strip()
                headers_dict[current_h4] = {}
                current_h5 = None
                current_h6 = None
                current_subauthor = None

            elif element.name == 'h5' and current_h4:
                current_h5 = element.get_text().strip()
                headers_dict[current_h4][current_h5] = {}
                current_h6 = None
                current_subauthor = None

            elif element.name == 'h6' and current_h4 and current_h5:
                current_h6 = element.get_text().strip()
                headers_dict[current_h4][current_h5][current_h6] = []
                current_subauthor = None

            elif element.name == 'p' and current_h6 and 'subAuthor' in element.get('class', []):
                current_subauthor = element.get_text().strip()

            elif element.name == 'dl' and current_h6:
                for dt in element.find_all('dt'):
                    entry = {}
                    dt_text = dt.get_text(separator=' ').strip()

                    # Extraer el código usando una expresión regular
                    code_match = re.search(r'\[Cód\. (\d+-\d+)\]', dt_text)
                    if code_match:
                        code = code_match.group(1)
                        dt_text = dt_text.replace(
                            code_match.group(0), '').strip()
                        self.cods.append(code)  # añadir a lista de códigos
                    else:
                        code = 'N/A'

                    entry['description'] = dt_text
                    entry['code'] = code
                    if current_subauthor:
                        entry['subauthor'] = current_subauthor

                    headers_dict[current_h4][current_h5][current_h6].append(
                        entry)

        return headers_dict

    def get_sumario(self):
        """
        Devuelve el sumario del boletín.

        Devuelve
        ---------
        dict
            Un diccionario que contiene el sumario del boletín.
        """
        return self.sumario

    def crear_json(self, filename=None):
        """
        Crea un archivo JSON con el contenido del boletín.

        Parámetros
        ----------
        filename : str, opcional
            El nombre del archivo JSON a crear. Si no se proporciona, se generará un nombre predeterminado.
        """

        if filename is None:
            # Formatear la fecha en el formato deseado: yy_mm_dd
            formatted_date = self.fecha.strftime("%y_%m_%d")
            # Nombre predeterminado del archivo JSON
            filename = f"BOPA-Boletin-{formatted_date}_sumario"

        # Ignorar el sufijo ".json" si existe
        if not filename.endswith(".json"):
            # Añadir el sufijo ".json" al nombre del archivo
            filename += ".json"

        # Convertir a un JSON con indentación para que sea legible
        json_content = json.dumps(self.sumario, ensure_ascii=False, indent=4)

        # Escribir el contenido con el archivo
        with open(filename, "w", encoding="utf-8") as file:
            file.write(json_content)

    def get_cod_disposiciones(self):
        """
        Devuelve una lista de los códigos de las disposiciones del boletín.

        Devuelve
        ---------
        list
            Una lista de los códigos de las disposiciones del boletín.
        """
        return self.cods

    def _get_disposiciones(self):
        """
        Obtiene las disposiciones del boletín de sede.asturias.

        Devuelve
        ---------
        list
            Una lista de objetos Disposicion que representan las disposiciones del boletín.
        """

        # ' Si las disposiciones no han sido obtenidas previamente, se obtienen
        # ' iterando sobre los códigos de disposición y creando una instancia de
        # ' la clase Disposicion para cada código. Las disposiciones obtenidas se
        # ' almacenan en la lista self.disposiciones.

        if not self.disposiciones:
            # print("Obteniendo disposiciones...")
            for code in self.cods:
                disposicion = Disposicion(
                    cod=code, num=self.num, fecha=self.fecha)
                self.disposiciones.append(disposicion)
        return self.disposiciones

    def get_disposiciones(self, nombre_archivo=None):
        """
        Obtiene las disposiciones del boletín y devuelve un JSON que concatena todos los JSON de las disposiciones.

        Parámetros
        ----------
        nombre_archivo : str, opcional
            Nombre del archivo donde se guardará el JSON concatenado (por defecto es None).

        Devuelve
        ---------
        str
            Un JSON que concatena todos los JSON de las disposiciones.
        """
        if not self.disposiciones:
            self._get_disposiciones()

        disposiciones_json = [json.loads(str(disposicion))
                                for disposicion in self.disposiciones]
        json_concatenado = json.dumps(
            disposiciones_json, ensure_ascii=False, indent=4)

        if nombre_archivo:
            with open(nombre_archivo, 'w', encoding='utf-8') as file:
                file.write(json_concatenado)
            print(f"JSON concatenado guardado en {nombre_archivo}")

        return json_concatenado
