"""Lee Datos y Notas como texto, valida esquema y filas, escribe 01_ingesta.csv y 01_notas.csv.

Ejecutar desde la raiz: python src/migracion/01_ingesta.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ingesta, seleccion, normalizacion, tipado, mensual_migracion

if __name__ == "__main__":
    ingesta('migracion')
