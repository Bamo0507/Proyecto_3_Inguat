"""Lee 01_ingesta.csv, selecciona poblacion/territorio/columnas y escribe 02_seleccion.csv.

Ejecutar desde la raiz: python src/movilidad_diaria/02_seleccion.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ingesta, seleccion, normalizacion, tipado, mensual_migracion

if __name__ == "__main__":
    seleccion('movilidad_diaria')
