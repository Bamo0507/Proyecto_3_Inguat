"""
Etapa 1 del pipeline: INGESTA
------------------------------------------------------------
Una sola responsabilidad: carga fiel de la fuente como texto de movilidad_diaria.

  Lee : data/raw/BD_moviidad_diario.xlsx
  Hace: aplica el contrato de ingesta para esta fuente.
  Escribe: data/processed/movilidad_diaria/01_ingesta.csv

Ejecutar: python src/movilidad_diaria/01_ingesta.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import FUENTES, COLUMNAS_ETAPA
from utils import leer_raw, guardar, esquema, filas

NOMBRE = 'movilidad_diaria'


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
