"""Lee 04_tipado.csv, agrega a rejilla mensual y escribe 05_mensual.csv y ventanas historicas.

Ejecutar desde la raiz: python src/migracion/05_mensual.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ingesta, seleccion, normalizacion, tipado, mensual_migracion

if __name__ == "__main__":
    mensual_migracion()
