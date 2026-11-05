"""Ejecuta todos los pipelines o uno. Uso: python src/run_pipeline.py [fuente]."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from config import FUENTES, RAW, PROCESSED

parser=argparse.ArgumentParser()
parser.add_argument('fuente',nargs='?',choices=['todas',*FUENTES,'dinamica_temporal'],default='todas')
args=parser.parse_args()
reporte={}
fuentes = FUENTES if args.fuente == 'todas' else [] if args.fuente == 'dinamica_temporal' else [args.fuente]
for fuente in fuentes:
    origen=RAW/FUENTES[fuente]['archivo']
    huella_antes=hashlib.sha256(origen.read_bytes()).hexdigest()
    for etapa in FUENTES[fuente]['etapas']:
        subprocess.run([sys.executable,str(Path(__file__).parent/fuente/f'{etapa}.py')],check=True)
    huella_despues=hashlib.sha256(origen.read_bytes()).hexdigest()
    if huella_antes!=huella_despues:
        raise RuntimeError(f'{fuente}: la fuente original cambio durante la ejecucion')
    reporte[fuente]={'sha256_raw':huella_despues,'etapas':FUENTES[fuente]['etapas'],'archivos_csv':sorted(p.name for p in (PROCESSED/fuente).glob('*.csv'))}
    (PROCESSED/fuente/'informe_ejecucion.json').write_text(json.dumps(reporte[fuente],ensure_ascii=False,indent=2)+'\n')

if args.fuente in ('todas', 'dinamica_temporal'):
    etapa = Path(__file__).parent / 'dinamica_temporal' / '01_series_municipales.py'
    subprocess.run([sys.executable, str(etapa)], check=True)
