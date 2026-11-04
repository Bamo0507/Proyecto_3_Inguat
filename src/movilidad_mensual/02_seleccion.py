"""
Etapa 2 del pipeline: SELECCION
------------------------------------------------------------
Una sola responsabilidad: seleccion de poblacion y columnas de movilidad_mensual.

  Lee : data/processed/movilidad_mensual/01_ingesta.csv
  Hace: aplica el contrato de seleccion para esta fuente.
  Escribe: data/processed/movilidad_mensual/02_seleccion.csv

Ejecutar: python src/movilidad_mensual/02_seleccion.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import FUENTES, MUNICIPIOS, COLUMNAS_ETAPA
from utils import leer, guardar, exigir, esquema

NOMBRE = 'movilidad_mensual'


def main():
    nombre = NOMBRE
    df = leer(nombre, '01_ingesta')
    esquema(df, COLUMNAS_ETAPA[nombre]['01_ingesta'])
    esquema(df, FUENTES[nombre]['columnas'])
    esperados = MUNICIPIOS if nombre == 'movilidad_mensual' else {m.upper() for m in MUNICIPIOS}
    exigir(set(df['destino']) == esperados, f'{nombre}: municipios inesperados')
    exigir(df['sub_grupo'].nunique() == 1, f'{nombre}: sub_grupo no constante')
    df = df.drop(columns=['sub_grupo'])
    esquema(df, COLUMNAS_ETAPA[nombre]['02_seleccion'])
    guardar(df, nombre, '02_seleccion')


if __name__ == "__main__":
    main()
