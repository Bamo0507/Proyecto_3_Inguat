"""
Etapa 3 del pipeline: NORMALIZACION
------------------------------------------------------------
Una sola responsabilidad: normalizacion documentada de categorias de migracion.

  Lee : data/processed/migracion/02_seleccion.csv
  Hace: aplica el contrato de normalizacion para esta fuente.
  Escribe: data/processed/migracion/03_normalizacion.csv

Ejecutar: python src/migracion/03_normalizacion.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import unicodedata
import pandas as pd
from config import FUENTES, VIAS, COLUMNAS_ETAPA
from utils import leer, guardar, exigir, esquema, nulos, incidencia

NOMBRE = 'migracion'


def main():
    nombre = NOMBRE
    df = leer(nombre, '02_seleccion')
    esquema(df, COLUMNAS_ETAPA[nombre]['02_seleccion'])
    fuente = leer(nombre, '01_ingesta')
    identificador = fuente.reset_index().rename(columns={'index': 'indice_origen'})
    identificador['indice_origen'] = identificador['indice_origen'] + 2
    claves = list(FUENTES[nombre]['columnas'])
    df = df.merge(identificador[claves + ['indice_origen']], on=claves, how='left', validate='one_to_one', sort=False)
    exigir(df['indice_origen'].notna().all(), 'Fila de origen sin traza')
    incidencias = []
    def agregar(mask, col, anterior, nuevo, motivo):
        for i in df.index[mask.fillna(False)]:
            incidencias.append({'fila_excel': int(df.at[i, 'indice_origen']), 'columna': col, 'valor_original': str(anterior.loc[i]), 'valor_normalizado': str(nuevo.loc[i]), 'motivo': motivo})
    codigo = df['Frontera'].str.extract('^(\\d{2})\\s', expand=False)
    via_esperada = codigo.map(VIAS)
    via_esperada = via_esperada.where(codigo.notna(), df['Frontera'].map({'Cruceros': 'Marítima'}))
    exigir(via_esperada.notna().all(), 'Frontera sin via en catalogo')
    reparacion = df['Vía'].ne(via_esperada)
    exigir(int(reparacion.sum()) == 92, 'Vias discrepantes en la poblacion seleccionada')
    agregar(reparacion, 'via', df['Vía'], via_esperada, 'catalogo_frontera')
    df['Vía'] = via_esperada
    normal = df['País'].map(lambda x: unicodedata.normalize('NFC', str(x)).strip().casefold())
    normal_fuente = fuente['País'].map(lambda x: unicodedata.normalize('NFC', str(x)).strip().casefold())
    canon = fuente.groupby(normal_fuente, sort=False)['País'].first()
    pais_nuevo = normal.map(canon)
    pais_cambio = df['País'].ne(pais_nuevo)
    agregar(pais_cambio, 'pais', df['País'], pais_nuevo, 'variante_mayusculas')
    mapa_paises = pd.DataFrame({'pais_original': df.loc[pais_cambio, 'País'], 'pais_normalizado': pais_nuevo.loc[pais_cambio]}).drop_duplicates().sort_values('pais_original')
    guardar(mapa_paises, nombre, 'mapa_paises')
    df['País'] = pais_nuevo
    residencia_nueva = df['Agrupación Residencia'].replace({'Resto de mundo': 'Resto del Mundo'})
    agregar(df['Agrupación Residencia'].ne(residencia_nueva), 'agrupacion_residencia', df['Agrupación Residencia'], residencia_nueva, 'variante_escritura')
    df['Agrupación Residencia'] = residencia_nueva
    for col, valor in [('Región dos', '0'), ('Regiones OMT', '0x2a')]:
        mask = df[col].eq(valor)
        nuevo = df[col].mask(mask)
        agregar(mask, {'Región dos': 'region_dos', 'Regiones OMT': 'regiones_omt'}[col], df[col], nuevo, 'clasificacion_invalida')
        df[col] = nuevo
    for col in ['País', 'Región', 'Región dos', 'Regiones OMT', 'MCEO', 'Agrupación Residencia']:
        df[col] = nulos(df[col])
    llave = ['Año', 'Mes cod', 'Vía', 'Frontera', 'País', 'Tipo de Viajero', 'Agrupación Residencia']
    colisiones = df.duplicated(llave, keep=False)
    exigir(int(colisiones.sum()) == 40, 'Colisiones normalizadas distintas de las 40 documentadas')
    for i in df.index[colisiones]:
        anterior = fuente.iloc[int(df.at[i, 'indice_origen']) - 2]
        incidencias.append({'fila_excel': int(df.at[i, 'indice_origen']), 'columna': 'clave_completa', 'valor_original': json.dumps({c: str(anterior[c]) for c in llave}, ensure_ascii=False), 'valor_normalizado': json.dumps({c: str(df.at[i, c]) for c in llave}, ensure_ascii=False), 'motivo': 'colision_conocida_conservada'})
    for col in ['Región dos', 'Regiones OMT']:
        esperado = 13 if col == 'Región dos' else 5
        exigir(int(df[col].isna().sum()) == esperado, f'{col}: invalidos inesperados')
    evidencia = pd.DataFrame(incidencias).sort_values(['fila_excel', 'columna'])
    incidencia(nombre, evidencia)
    esquema(df, COLUMNAS_ETAPA[nombre]['03_normalizacion'])
    guardar(df, nombre, '03_normalizacion')


if __name__ == "__main__":
    main()
