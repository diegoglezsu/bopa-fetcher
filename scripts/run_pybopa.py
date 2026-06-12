"""Small script to query BOPA data using the pybopa library."""

import sys

from pybopa.api import Client


def main() -> int:

    fecha = sys.argv[1]
    client = Client()

    print(f"\n=== get_boletin({fecha}) ===")
    boletin = client.get_boletin(fecha)
    print(f"  num: {boletin.num}")
    print(f"  fecha: {boletin.fecha}")
    print(f"  sumario keys: {list(boletin.sumario.keys())}")
    print(f"  disposiciones count: {len(boletin.disposiciones)}")
    if boletin.disposiciones:
        print(f"  primera disposicion: {boletin.disposiciones[0].cod}, {boletin.disposiciones[0].num}, {boletin.disposiciones[0].fecha}, {boletin.disposiciones[0].contenido[:100] if boletin.disposiciones[0].contenido else 'empty'}...")

    print(f"\n=== get_sumario({fecha}) ===")
    sumario = client.get_sumario(fecha)
    print(f"  type: {type(sumario).__name__}")
    print(f"  keys: {list(sumario.keys())[:3]}...")

    print(f"\n=== get_disposicion(cod='2024-03997', num='1', fecha='13/05/2024') ===")
    disp = client.get_disposicion(cod="2024-03997", num="1", fecha="13/05/2024")
    print(f"  cod: {disp.cod}")
    print(f"  contenido (first 100 chars): {disp.contenido[0][:100] if disp.contenido else 'empty'}")

    print(f"\n=== get_boletines(desde='{fecha}', hasta='{fecha}') ===")
    boletines = client.get_boletines(fecha, fecha)
    print(f"  count: {len(boletines)}")
    if boletines:
        print(f"  first num: {boletines[0].num}")

    print(f"\n=== get_disposiciones(desde='{fecha}', hasta='{fecha}') ===")
    disposiciones = client.get_disposiciones(fecha, fecha)
    print(f"  count: {len(disposiciones)}")
    if disposiciones:
        print(f"  first: {disposiciones[0][:100]}...")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
