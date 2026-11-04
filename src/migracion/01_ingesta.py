"""
Etapa 1 del pipeline: INGESTA
------------------------------------------------------------
Una sola responsabilidad: carga fiel de la fuente como texto de migracion.

  Lee : data/raw/Base_Migracion_2009-2026jun.xlsx
  Hace: aplica el contrato de ingesta para esta fuente.
  Escribe: data/processed/migracion/01_ingesta.csv

Ejecutar: python src/migracion/01_ingesta.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from openpyxl import load_workbook
from config import FUENTES, RAW, COLUMNAS_ETAPA
from utils import leer_raw, guardar, exigir, esquema, filas

NOMBRE = 'migracion'


def main():
    nombre = NOMBRE
    df = leer_raw(nombre)
    esquema(df, FUENTES[nombre]['columnas'])
    esperado = FUENTES[nombre]['filas_raw']
    filas(df, esperado, f'{nombre}: ingesta')
    esquema(df, COLUMNAS_ETAPA[nombre]['01_ingesta'])
    guardar(df, nombre, '01_ingesta')
    libro = load_workbook(RAW / FUENTES[nombre]['archivo'], read_only=True, data_only=True)
    try:
        hoja = libro['Notas']
        hoja.reset_dimensions()
        notas = []
        for numero, valores in enumerate(hoja.iter_rows(values_only=True), start=1):
            notas.append({'fila_excel': numero, 'tema': '' if len(valores) < 1 or valores[0] is None else str(valores[0]), 'descripcion': '' if len(valores) < 2 or valores[1] is None else str(valores[1])})
        exigir(len(notas) == 10, 'Hoja Notas: filas inesperadas')
        guardar(pd.DataFrame(notas), nombre, '01_notas')
    finally:
        libro.close()


if __name__ == "__main__":
    main()
