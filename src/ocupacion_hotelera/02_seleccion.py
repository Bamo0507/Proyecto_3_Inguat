"""
Etapa 2 del pipeline: SELECCION
------------------------------------------------------------
Una sola responsabilidad: seleccion de poblacion y columnas de ocupacion_hotelera.

  Lee : data/processed/ocupacion_hotelera/01_ingesta.csv
  Hace: aplica el contrato de seleccion para esta fuente.
  Escribe: data/processed/ocupacion_hotelera/02_seleccion.csv

Ejecutar: python src/ocupacion_hotelera/02_seleccion.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import FUENTES, COLUMNAS_ETAPA
from utils import leer, guardar, exigir, esquema, filas, clave

NOMBRE = 'ocupacion_hotelera'


def main():
    nombre = NOMBRE
    df = leer(nombre, '01_ingesta')
    esquema(df, COLUMNAS_ETAPA[nombre]['01_ingesta'])
    esquema(df, FUENTES[nombre]['columnas'])
    df = df.loc[df['departamento'].eq('Sololá')].copy()
    filas(df, FUENTES[nombre]['filas'], f'{nombre}: Solola')
    exigir(df['departamento'].eq('Sololá').all(), 'Filtro de departamento fallido')
    clave(df, ['anio', 'mes', 'departamento'], nombre)
    esquema(df, COLUMNAS_ETAPA[nombre]['02_seleccion'])
    guardar(df, nombre, '02_seleccion')


if __name__ == "__main__":
    main()
