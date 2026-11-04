"""
Etapa 1 del pipeline: INGESTA
------------------------------------------------------------
Una sola responsabilidad: carga fiel de la fuente como texto de ocupacion_hotelera.

  Lee : data/raw/indice_ocupacion_mensual_2023_2025_1.csv
  Hace: aplica el contrato de ingesta para esta fuente.
  Escribe: data/processed/ocupacion_hotelera/01_ingesta.csv

Ejecutar: python src/ocupacion_hotelera/01_ingesta.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import FUENTES, COLUMNAS_ETAPA
from utils import leer_raw, guardar, esquema, filas

NOMBRE = 'ocupacion_hotelera'


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
