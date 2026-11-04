"""
Etapa 3 del pipeline: NORMALIZACION
------------------------------------------------------------
Una sola responsabilidad: normalizacion documentada de categorias de movilidad_mensual.

  Lee : data/processed/movilidad_mensual/02_seleccion.csv
  Hace: aplica el contrato de normalizacion para esta fuente.
  Escribe: data/processed/movilidad_mensual/03_normalizacion.csv

Ejecutar: python src/movilidad_mensual/03_normalizacion.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import COLUMNAS_ETAPA
from utils import leer, guardar, exigir, esquema, nulos

NOMBRE = 'movilidad_mensual'


def main():
    nombre = NOMBRE
    df = leer(nombre, '02_seleccion')
    esquema(df, COLUMNAS_ETAPA[nombre]['02_seleccion'])
    df['pais'] = nulos(df['pais'])
    exigir(int(df['pais'].isna().sum()) == 25, 'Pais mensual: faltantes inesperados')
    esquema(df, COLUMNAS_ETAPA[nombre]['03_normalizacion'])
    guardar(df, nombre, '03_normalizacion')


if __name__ == "__main__":
    main()
