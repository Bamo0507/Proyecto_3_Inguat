"""
Etapa 5 del pipeline: MENSUAL
------------------------------------------------------------
Una sola responsabilidad: agregacion mensual de ingresos de migracion.

  Lee : data/processed/migracion/04_tipado.csv
  Hace: aplica el contrato de mensual para esta fuente.
  Escribe: data/processed/migracion/05_mensual.csv

Ejecutar: python src/migracion/05_mensual.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from decimal import Decimal
import pandas as pd
from config import SALIDAS_FINALES, COLUMNAS_ETAPA, FORMATO_FECHA
from utils import leer, guardar, exigir, esquema, decimal

NOMBRE = 'migracion'


def main():
    nombre = NOMBRE
    df = leer(nombre, '04_tipado')
    esquema(df, COLUMNAS_ETAPA[nombre]['04_tipado'])
    df['viajeros'] = decimal(df['viajeros'], 'viajeros', 0)
    df['viajeros_decimal'] = df['viajeros'].map(Decimal)
    fechas = pd.date_range('2009-01-01', '2026-06-01', freq='MS').strftime(FORMATO_FECHA)
    agregado = df.groupby('fecha').agg(viajeros=('viajeros_decimal', 'sum'), registros=('viajeros', 'size')).reindex(fechas)
    agregado.index.name = 'fecha'
    agregado.loc[agregado['registros'].isna(), 'viajeros'] = pd.NA
    agregado['registros'] = agregado['registros'].fillna(0).astype('Int64')
    agregado = agregado.reset_index()
    agregado['conjunto'] = 'historico'
    agregado.loc[agregado['fecha'].between('2023-01-01', '2025-12-01'), 'conjunto'] = 'ajuste'
    agregado.loc[agregado['fecha'].between('2026-01-01', '2026-06-01'), 'conjunto'] = 'evaluacion'
    exigir(len(agregado) == 210 and int(agregado['viajeros'].isna().sum()) == 5, 'Rejilla mensual migracion')
    exigir(agregado.loc[agregado['conjunto'].isin(['ajuste', 'evaluacion']), 'viajeros'].gt(0).all(), 'Ventana no positiva')
    exigir(int((agregado['conjunto'] == 'ajuste').sum()) == 36 and int((agregado['conjunto'] == 'evaluacion').sum()) == 6, 'Ventanas migracion')
    exigir(sum((v for v in agregado['viajeros'] if pd.notna(v)), Decimal(0)) == sum(df['viajeros_decimal'], Decimal(0)), 'Suma migracion no concilia')
    agregado['viajeros'] = agregado['viajeros'].map(lambda v: str(v) if pd.notna(v) else pd.NA)
    esquema(agregado, COLUMNAS_ETAPA[nombre]['05_mensual'])
    guardar(agregado, nombre, '05_mensual')
    guardar(agregado, nombre, SALIDAS_FINALES[nombre][1])
    guardar(agregado.loc[agregado['conjunto'] == 'ajuste'], nombre, SALIDAS_FINALES[nombre][2])
    guardar(agregado.loc[agregado['conjunto'] == 'evaluacion'], nombre, SALIDAS_FINALES[nombre][3])


if __name__ == "__main__":
    main()
