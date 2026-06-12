from datetime import datetime, timedelta

from ..boletin import Boletin
from ..disposicion import Disposicion
from ..biblioteca import Biblioteca


class Client:
    def get_boletin(self, fecha: str) -> Boletin:
        boletin = Boletin(fecha=fecha)
        boletin._get_disposiciones()
        return boletin

    def get_boletines(self, desde: str, hasta: str) -> list[Boletin]:
        fecha_desde = datetime.strptime(desde, "%d/%m/%Y")
        fecha_hasta = datetime.strptime(hasta, "%d/%m/%Y")

        boletines = []
        fecha_actual = fecha_desde
        while fecha_actual <= fecha_hasta:
            fecha_str = fecha_actual.strftime("%d/%m/%Y")
            try:
                boletines.append(self.get_boletin(fecha_str))
            except Exception:
                pass
            fecha_actual += timedelta(days=1)

        return boletines

    def get_disposicion(self, cod: str, num: str, fecha: str) -> Disposicion:
        return Disposicion(cod=cod, num=num, fecha=datetime.strptime(fecha, "%d/%m/%Y"))

    def get_sumario(self, fecha: str) -> dict:
        boletin = Boletin(fecha=fecha)
        return boletin.get_sumario()

    def get_disposiciones(self, desde: str, hasta: str, archivo_json: str = None) -> list[dict]:
        biblioteca = Biblioteca()
        boletines = self.get_boletines(desde, hasta)
        for b in boletines:
            biblioteca.agregar_boletin(b)
        biblioteca.obtener_disposiciones(desde, hasta, archivo_json)
        disposiciones = []
        for b in boletines:
            disposiciones.extend(b.disposiciones)
        return [str(d) for d in disposiciones]
