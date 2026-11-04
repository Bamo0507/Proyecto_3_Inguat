"""Lee 02_seleccion.csv, tipa y valida el contrato final, escribe 03_tipado.csv y tabla final.

Ejecutar desde la raiz: python src/ocupacion_hotelera/03_tipado.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ingesta, seleccion, normalizacion, tipado, mensual_migracion

if __name__ == "__main__":
    tipado('ocupacion_hotelera')
