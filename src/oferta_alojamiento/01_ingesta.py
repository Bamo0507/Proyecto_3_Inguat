"""
Etapa 1 del pipeline: INGESTA
------------------------------------------------------------
Una sola responsabilidad: carga fiel de la fuente como texto de oferta_alojamiento.

  Lee : data/raw/oferta_hotelera_2022_2026.csv
  Hace: aplica el contrato de ingesta para esta fuente.
  Escribe: data/processed/oferta_alojamiento/01_ingesta.csv

Ejecutar: python src/oferta_alojamiento/01_ingesta.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import FUENTES, COLUMNAS_ETAPA
from utils import leer_raw, guardar, esquema, filas

NOMBRE = 'oferta_alojamiento'


def main():
    nombre = NOMBRE
    df = leer_raw(nombre)
    esquema(df, FUENTES[nombre]['columnas'])
    esperado = FUENTES[nombre]['filas_raw']
    filas(df, esperado, f'{nombre}: ingesta')
    esquema(df, COLUMNAS_ETAPA[nombre]['01_ingesta'])
    guardar(df, nombre, '01_ingesta')


if __name__ == "__main__":
    main()
