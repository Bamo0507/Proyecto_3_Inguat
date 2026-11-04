"""
Etapa 4 del pipeline: TIPADO
------------------------------------------------------------
Una sola responsabilidad: conversion y validacion de tipos de migracion.

  Lee : data/processed/migracion/03_normalizacion.csv
  Hace: aplica el contrato de tipado para esta fuente.
  Escribe: data/processed/migracion/04_tipado.csv

Ejecutar: python src/migracion/04_tipado.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from config import MESES, SALIDAS_FINALES, COLUMNAS_SALIDA, COLUMNAS_ETAPA, FORMATO_FECHA
from utils import leer, guardar, exigir, esquema, filas, entero, decimal

NOMBRE = 'migracion'


def main():
    nombre = NOMBRE
    etapa = '03_normalizacion'
    df = leer(nombre, etapa)
    esquema(df, COLUMNAS_ETAPA[nombre]['03_normalizacion'])
    df = df.rename(columns={'Año': 'anio', 'Mes cod': 'mes', 'Vía': 'via', 'Frontera': 'frontera', 'País': 'pais', 'Región': 'region', 'Región dos': 'region_dos', 'Regiones OMT': 'regiones_omt', 'MCEO': 'mceo', 'Agrupación Residencia': 'agrupacion_residencia', 'Tipo de Viajero': 'tipo_viajero', 'Viajero': 'viajeros'})
    df['anio'] = entero(df['anio'], 'anio', 2009, 2026)
    df['mes'] = entero(df['mes'], 'mes', 1, 12)
    exigir((df['Mes'] == df['mes'].map(MESES)).all(), 'Nombre de mes incoherente')
    df['fecha'] = pd.to_datetime(dict(year=df['anio'], month=df['mes'], day=1)).dt.strftime(FORMATO_FECHA)
    df['viajeros'] = decimal(df['viajeros'], 'viajeros', 0)
    df = df.drop(columns=['Mes', 'indice_origen'])
    df = df[COLUMNAS_SALIDA[nombre]]
    exigir(set(df['tipo_viajero']) == {'Turista', 'Excursionista'} and (not df['pais'].eq('Guatemala').any()), 'Poblacion migracion')
    filas(df, 132894, nombre)
    esquema(df, COLUMNAS_ETAPA[nombre]['04_tipado'])
    guardar(df, nombre, '04_tipado')
    guardar(df, nombre, SALIDAS_FINALES[nombre][0])


if __name__ == "__main__":
    main()
