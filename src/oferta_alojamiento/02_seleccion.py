"""Lee 01_ingesta.csv, selecciona poblacion/territorio/columnas y escribe 02_seleccion.csv.

Ejecutar desde la raiz: python src/oferta_alojamiento/02_seleccion.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ingesta, seleccion, normalizacion, tipado, mensual_migracion

if __name__ == "__main__":
    seleccion('oferta_alojamiento')
