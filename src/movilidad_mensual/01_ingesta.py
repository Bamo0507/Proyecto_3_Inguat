"""Lee la fuente original como texto, valida esquema y filas, escribe 01_ingesta.csv.

Ejecutar desde la raiz: python src/movilidad_mensual/01_ingesta.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ingesta, seleccion, normalizacion, tipado, mensual_migracion

if __name__ == "__main__":
    ingesta('movilidad_mensual')
