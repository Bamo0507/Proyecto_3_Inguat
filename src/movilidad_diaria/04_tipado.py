"""
Etapa 4 del pipeline: TIPADO
------------------------------------------------------------
Una sola responsabilidad: conversion y validacion de tipos de movilidad_diaria.

  Lee : data/processed/movilidad_diaria/03_normalizacion.csv
  Hace: aplica el contrato de tipado para esta fuente.
  Escribe: data/processed/movilidad_diaria/04_tipado.csv

Ejecutar: python src/movilidad_diaria/04_tipado.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unicodedata
from config import SALIDAS_FINALES, COLUMNAS_ETAPA, FORMATO_FECHA_HORA
from utils import leer, guardar, exigir, esquema, filas, clave, entero, decimal, fecha

NOMBRE = 'movilidad_diaria'


def main():
    nombre = NOMBRE
    etapa = '03_normalizacion'
    df = leer(nombre, etapa)
    esquema(df, COLUMNAS_ETAPA[nombre]['03_normalizacion'])
    df = df.rename(columns={'Week': 'num_semana'})
    for c, lo, hi in [('anio', 2025, 2026), ('mes', 1, 12), ('num_semana', 1, 53)]:
        df[c] = entero(df[c], c, lo, hi)
    d = fecha(df['idfecha'], 'idfecha')
    exigir((d.dt.year == df['anio']).all() and (d.dt.month == df['mes']).all(), 'Fecha diaria incoherente')
    exigir((d.dt.isocalendar().week.astype('Int64') == df['num_semana']).all(), 'Semana ISO incoherente')
    dias = {0: 'lunes', 1: 'martes', 2: 'miercoles', 3: 'jueves', 4: 'viernes', 5: 'sabado', 6: 'domingo'}
    normal = lambda x: ''.join((c for c in unicodedata.normalize('NFKD', str(x).casefold()) if not unicodedata.combining(c)))
    exigir((df['dia_semana'].map(normal) == d.dt.dayofweek.map(dias)).all(), 'Dia de semana incoherente')
    df['idfecha'] = d.dt.strftime(FORMATO_FECHA_HORA)
    df['cantidad_visitantes'] = decimal(df['cantidad_visitantes'], 'cantidad_visitantes', 0)
    clave(df, ['destino', 'idfecha', 'pais'], nombre)
    filas(df, 82952, nombre)
    esquema(df, COLUMNAS_ETAPA[nombre]['04_tipado'])
    guardar(df, nombre, '04_tipado')
    guardar(df, nombre, SALIDAS_FINALES[nombre][0])


if __name__ == "__main__":
    main()
