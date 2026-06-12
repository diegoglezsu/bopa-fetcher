# &p_r_p_dispositionReference=2024-03997&p_r_p_dispositionDate=13%2F05%2F2024

import requests
import re
import json
from bs4 import BeautifulSoup
from datetime import datetime


class Disposicion:
    """
    Una clase para representar un Boletín Oficial del Principado de Asturias (BOPA).

    Atributos
    ----------
    cod : str
        El código del boletín.
    num : str
        El número del boletín.
    fecha : datetime
        La fecha del boletín.
    contenido : list
        El contenido parseado del boletín.
    """

    def __init__(self, cod=None, num=None, fecha=None):
        """
        Construye todos los atributos necesarios para el objeto Boletin.

        Parameters
        ----------
        cod : str, opcional
            El código del boletín (por defecto es None).
        num : str, opcional
            El número del boletín (por defecto es None).
        fecha : datetime, opcional
            La fecha del boletín (por defecto es None).
        """
        self.cod = cod
        self.num = num
        self.fecha = fecha
        self.contenido = self._get_disposicion()

    def _get_disposicion(self):
        """
        Obtiene y parsea el contenido del boletín desde la URL especificada.

        Devuelve
        ---------
        list
            Una lista con el contenido del boletín.
        """

        url = f"https://sede.asturias.es/ast/bopa-disposiciones?p_p_id=pa_sede_bopa_web_portlet_SedeBopaDispositionWeb&p_p_lifecycle=0&_pa_sede_bopa_web_portlet_SedeBopaDispositionWeb_mvcRenderCommandName=%2Fdisposition%2Fdetail&p_r_p_dispositionText={
            self.cod}&p_r_p_dispositionReference={self.cod}&p_r_p_dispositionDate={self.fecha.strftime("%d%%2F%m%%2F%Y")}"

        # print(f"Consultando {url}")

        # Obtener el contenido HTML de la página
        response = requests.get(url, timeout=60)
        print(response)
        html_content = response.content

        # Parsear el HTML usando BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Encontrar el elemento div con id="bopa-boletin"
        texto_disposicion = soup.find("div", {"id": "bopa-articulo"})

        # Inicializar una lista para almacenar los textos
        text_list = []

        # Recorrer todos los elementos dentro del div
        for element in texto_disposicion.find_all():
            # Extraer el texto del elemento y agregarlo a la lista
            text_list.append(element.get_text(separator=' '))

        # Filtrar elementos vacíos
        text_list = [text for text in text_list if text.strip()]

        return (text_list)

    def _sacar_num_y_fecha(self, text):
        """
        Extrae el número de código y la fecha del texto proporcionado.

        Parameters
        ----------
        text : str
            El texto del cual extraer el número de código y la fecha.

        Devuelve
        ---------
        None
        """

        # Define el patrón de expresión regular para encontrar el número de código y la fecha
        pattern = r"Nº (\d+) del ([0-9]+) de (\w+) de (\d{4})"

        # Usa re.search para encontrar el patrón en el texto
        match = re.search(pattern, text)

        if match:
            code_number = match.group(1)
            day = match.group(2)
            month_str = match.group(3)
            year = match.group(4)

            # Convierte el nombre del mes a su número correspondiente
            month_dict = {
                "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
                "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
                "septiembre": "09", "octubre": "10", "noviembre": "11", 
                "diciembre": "12"
            }
            month = month_dict.get(month_str.lower(), "00")

            # Formatea la fecha
            formatted_date = f"{day}/{month}/{year}"

            print("Número de código:", code_number)
            print("Fecha:", formatted_date)
        else:
            print("Número de código y fecha no encontrados.")

    def get_contenido(self):
        """
        Devuelve el contenido de la disposición.

        Devuelve
        ---------
        list
            Una lista con el contenido del boletín.
        """
        return self.contenido

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto Boletin.

        Devuelve
        ---------
        str
            Una cadena JSON que representa el objeto Boletin.
        """
        
        # Formatear la fecha al formato dd/mm/YYYY
        formatted_fecha = self.fecha.strftime("%d/%m/%Y")

        # Estructurar el diccionario
        dict_representation = {
            "num": self.num,
            "fecha": formatted_fecha,
            "cod": self.cod,
            "contenido": self.contenido  # Asumiendo que contenido ya es una lista de strings
        }

        # Convertir el diccionario a una cadena JSON
        return json.dumps(dict_representation, ensure_ascii=False, indent=4)
    
    