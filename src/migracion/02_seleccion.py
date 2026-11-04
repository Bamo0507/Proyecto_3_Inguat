"""
Etapa 2 del pipeline: SELECCION
------------------------------------------------------------
Una sola responsabilidad: seleccion de poblacion y columnas de migracion.

  Lee : data/processed/migracion/01_ingesta.csv
  Hace: aplica el contrato de seleccion para esta fuente.
  Escribe: data/processed/migracion/02_seleccion.csv

Ejecutar: python src/migracion/02_seleccion.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import FUENTES, VIAS, COLUMNAS_ETAPA
from utils import leer, guardar, exigir, esquema, filas, clave

NOMBRE = 'migracion'


def main():
    nombre = NOMBRE
    df = leer(nombre, '01_ingesta')
    esquema(df, COLUMNAS_ETAPA[nombre]['01_ingesta'])
    esquema(df, FUENTES[nombre]['columnas'])
    clave(df, ['Año', 'Mes cod', 'Vía', 'Frontera', 'País', 'Tipo de Viajero', 'Agrupación Residencia'], 'migracion original')
    codigo = df['Frontera'].str.extract('^(\\d{2})\\s', expand=False)
    esperada = codigo.map(VIAS).where(codigo.notna(), df['Frontera'].map({'Cruceros': 'Marítima'}))
    exigir(esperada.notna().all() and int(df['Vía'].ne(esperada).sum()) == 93, 'Catalogo de vias de la fuente no concilia')
    exigir(set(df['Tipo de Viajero'].dropna()) == {'Turista', 'Excursionista', 'Viajero', 'Cruceristas'}, 'Tipos de viajero inesperados')
    tipos = df['Tipo de Viajero'].isin(['Turista', 'Excursionista'])
    exigir(int(tipos.sum()) == 137642, 'Filtro de tipos no concilia')
    df = df.loc[tipos & df['País'].ne('Guatemala')].copy()
    filas(df, 132894, 'migracion: poblacion objetivo')
    esquema(df, COLUMNAS_ETAPA[nombre]['02_seleccion'])
    guardar(df, nombre, '02_seleccion')


if __name__ == "__main__":
    main()
