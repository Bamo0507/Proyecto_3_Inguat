"""Lee 02_seleccion.csv, normaliza categorias y escribe 03_normalizacion.csv e incidencias si aplica.

Ejecutar desde la raiz: python src/movilidad_diaria/03_normalizacion.py
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pipeline import ingesta, seleccion, normalizacion, tipado, mensual_migracion

if __name__ == "__main__":
    normalizacion('movilidad_diaria')
