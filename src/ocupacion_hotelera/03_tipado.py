"""
Etapa 3 del pipeline: TIPADO
------------------------------------------------------------
Una sola responsabilidad: conversion y validacion de tipos de ocupacion_hotelera.

  Lee : data/processed/ocupacion_hotelera/02_seleccion.csv
  Hace: aplica el contrato de tipado para esta fuente.
  Escribe: data/processed/ocupacion_hotelera/03_tipado.csv

Ejecutar: python src/ocupacion_hotelera/03_tipado.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from config import SALIDAS_FINALES, COLUMNAS_ETAPA, FORMATO_FECHA
from utils import leer, guardar, exigir, esquema, filas, clave, entero, filas_origen, limpiar_cantidad, guardar_incidencias_cantidad

NOMBRE = 'ocupacion_hotelera'


def main():
    nombre = NOMBRE
    etapa = '02_seleccion'
    df = leer(nombre, etapa)
    esquema(df, COLUMNAS_ETAPA[nombre]['02_seleccion'])
    origen = filas_origen(df, nombre, ['anio', 'mes', 'departamento'])
    incidencias = []
    df['anio'] = entero(df['anio'], 'anio', 2023, 2025)
    df['mes'] = entero(df['mes'], 'mes', 1, 12)
    df['indice_ocupacion'] = limpiar_cantidad(df['indice_ocupacion'], 'indice_ocupacion', incidencias, origen, minimo=0, maximo=1)
    df['fecha'] = pd.to_datetime(dict(year=df['anio'], month=df['mes'], day=1)).dt.strftime(FORMATO_FECHA)
    df = df[['fecha', 'indice_ocupacion']]
    clave(df, ['fecha'], nombre)
    exigir(set(df['fecha']) == set(pd.date_range('2023-01-01', '2025-12-01', freq='MS').strftime('%Y-%m-%d')), 'Cobertura ocupacion')
    filas(df, 36, nombre)
    esquema(df, COLUMNAS_ETAPA[nombre]['03_tipado'])
    guardar_incidencias_cantidad(nombre, incidencias)
    guardar(df, nombre, '03_tipado')
    guardar(df, nombre, SALIDAS_FINALES[nombre][0])


if __name__ == "__main__":
    main()
