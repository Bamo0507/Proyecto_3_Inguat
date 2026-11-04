"""
Etapa 3 del pipeline: TIPADO
------------------------------------------------------------
Una sola responsabilidad: conversion y validacion de tipos de oferta_alojamiento.

  Lee : data/processed/oferta_alojamiento/02_seleccion.csv
  Hace: aplica el contrato de tipado para esta fuente.
  Escribe: data/processed/oferta_alojamiento/03_tipado.csv

Ejecutar: python src/oferta_alojamiento/03_tipado.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import TIPOS_ALOJAMIENTO, SALIDAS_FINALES, COLUMNAS_ETAPA
from utils import leer, guardar, exigir, esquema, filas, clave, entero, filas_origen, limpiar_cantidad, guardar_incidencias_cantidad

NOMBRE = 'oferta_alojamiento'


def main():
    nombre = NOMBRE
    etapa = '02_seleccion'
    df = leer(nombre, etapa)
    esquema(df, COLUMNAS_ETAPA[nombre]['02_seleccion'])
    origen = filas_origen(df, nombre, ['anio', 'trimestre', 'departamento', 'tipo_alojamiento'])
    incidencias = []
    df['anio'] = entero(df['anio'], 'anio', 2022, 2026)
    df['trimestre'] = entero(df['trimestre'], 'trimestre', 1, 4)
    for c in ['establecimientos', 'habitaciones', 'plazas_cama']:
        df[c] = limpiar_cantidad(df[c], c, incidencias, origen, minimo=0, entera=True)
    exigir(set(df['tipo_alojamiento']) == TIPOS_ALOJAMIENTO, 'Tipos de alojamiento inesperados')
    # La incoherencia se registra sin inventar cual de las dos cantidades corregir.
    for menor, mayor in [('habitaciones', 'establecimientos'), ('plazas_cama', 'habitaciones')]:
        incoherentes = (df[menor] < df[mayor]).fillna(False)
        for indice in df.index[incoherentes]:
            incidencias.append({
                'fila_csv': int(origen.loc[indice]), 'columna': menor,
                'valor_original': str(df.at[indice, menor]),
                'valor_normalizado': str(df.at[indice, menor]),
                'motivo': f'capacidad_menor_que_{mayor}', 'clasificacion': 'requiere_revision',
            })
    df = df.drop(columns=['departamento'])
    clave(df, ['anio', 'trimestre', 'tipo_alojamiento'], nombre)
    exigir(set(zip(df['anio'], df['trimestre'])) == {(2022, 4), (2023, 4), (2024, 4), (2025, 4), (2026, 1)}, 'Cortes inesperados')
    filas(df, 15, nombre)
    esquema(df, COLUMNAS_ETAPA[nombre]['03_tipado'])
    guardar_incidencias_cantidad(nombre, incidencias)
    guardar(df, nombre, '03_tipado')
    guardar(df, nombre, SALIDAS_FINALES[nombre][0])


if __name__ == "__main__":
    main()
