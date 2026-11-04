"""
Etapa 4 del pipeline: TIPADO
------------------------------------------------------------
Una sola responsabilidad: conversion y validacion de tipos de movilidad_mensual.

  Lee : data/processed/movilidad_mensual/03_normalizacion.csv
  Hace: aplica el contrato de tipado para esta fuente.
  Escribe: data/processed/movilidad_mensual/04_tipado.csv

Ejecutar: python src/movilidad_mensual/04_tipado.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import MUNICIPIOS, SALIDAS_FINALES, COLUMNAS_ETAPA, FORMATO_FECHA_HORA
from utils import leer, guardar, exigir, esquema, filas, clave, entero, decimal, fecha

NOMBRE = 'movilidad_mensual'


def main():
    nombre = NOMBRE
    etapa = '03_normalizacion'
    df = leer(nombre, etapa)
    esquema(df, COLUMNAS_ETAPA[nombre]['03_normalizacion'])
    df = df.drop(columns=['permanencia_prom'])
    df['anio'] = entero(df['anio'], 'anio', 2025, 2026)
    df['mes'] = entero(df['mes'], 'mes', 1, 12)
    d = fecha(df['fecha'], 'fecha')
    exigir((d.dt.year == df['anio']).all() and (d.dt.month == df['mes']).all(), 'Fecha mensual incoherente')
    df['fecha'] = d.dt.strftime(FORMATO_FECHA_HORA)
    for c in ['visitantes', 'dias_persona']:
        df[c] = decimal(df[c], c, 0)
    clave(df, ['destino', 'fecha', 'pais', 'es_consecutivo'], nombre)
    exigir(set(df['destino']) == MUNICIPIOS, 'Municipios mensuales')
    exigir(set(df['es_consecutivo']) == {'mayor a 1 dia', 'menor a 1 dia'}, 'Permanencia inesperada')
    filas(df, 9860, nombre)
    exigir(not ((df['anio'] == 2026) & df['mes'].isin([1, 2])).any(), 'Meses no observados agregados')
    esquema(df, COLUMNAS_ETAPA[nombre]['04_tipado'])
    guardar(df, nombre, '04_tipado')
    guardar(df, nombre, SALIDAS_FINALES[nombre][0])


if __name__ == "__main__":
    main()
