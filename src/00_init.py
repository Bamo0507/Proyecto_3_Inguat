"""Prepara el entorno. Ejecutar: python3 src/00_init.py [--python RUTA]."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from config import RAIZ

parser=argparse.ArgumentParser()
parser.add_argument('--python', default=shutil.which('python3.13') or sys.executable, help='Python base compatible (recomendado 3.13)')
args=parser.parse_args()
venv=RAIZ/'.venv'
subprocess.run([args.python,'-m','venv',str(venv)],check=True)
subprocess.run([str(venv/'bin'/'python'),'-m','pip','install','-r',str(RAIZ/'requirements.txt')],check=True)
print(f'Entorno listo: {venv}')
