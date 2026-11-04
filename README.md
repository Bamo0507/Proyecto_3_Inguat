# Preprocesamiento del Observatorio Turístico del Lago de Atitlán

Pipelines reproducibles para cinco fuentes. Requiere Python 3.13. No modifica `data/raw/`; escribe CSV e informes en `data/processed/<fuente>/`.

## Preparación

Desde la raíz del proyecto:

```bash
python3 src/00_init.py --python python3.13
```

En macOS/Linux, esto crea `.venv/` e instala `requirements.txt`. También se puede preparar manualmente:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Ejecución

```bash
.venv/bin/python src/run_pipeline.py
.venv/bin/python src/run_pipeline.py movilidad_mensual
.venv/bin/python src/run_pipeline.py movilidad_diaria
.venv/bin/python src/run_pipeline.py migracion
.venv/bin/python src/run_pipeline.py ocupacion_hotelera
.venv/bin/python src/run_pipeline.py oferta_alojamiento
```

Se puede ejecutar una etapa concreta desde la raíz, una vez que exista su entrada anterior:

```bash
.venv/bin/python src/migracion/03_normalizacion.py
```

El orden es `01_ingesta`, `02_seleccion`, `03_normalizacion` (si corresponde), `03_tipado` o `04_tipado`, y `05_mensual` solo para migración. Cada etapa valida su entrada y su salida; una discrepancia detiene el proceso. Los CSV numerados son intermediarios auditables. Las tablas sin número son las salidas finales descritas en [codebook.md](codebook.md). `informe_ejecucion.json` guarda la huella SHA-256 de la fuente y los archivos generados. `migracion/01_notas.csv` conserva la hoja de notas con números de fila Excel. `migracion/incidencias.csv` conserva correcciones y colisiones con fila Excel; `migracion/mapa_paises.csv` registra 13 equivalencias de escritura.

Los CSV usan UTF-8, coma como separador, punto decimal y `\N` como nulo. Las fechas se escriben `AAAA-MM-DD`; las fechas originales de movilidad incluyen `HH:MM:SS`. La ingesta conserva texto y marcadores originales; la normalización interpreta ausencias. Los valores numéricos se validan con `Decimal` y se escriben sin redondeo. Una celda con cero es un cero observado; una fila ausente no se fabrica. La serie mensual de migración sí tiene una rejilla explícita y deja `\N` en meses sin registros.

## Verificación

```bash
.venv/bin/python -m unittest discover -s tests -v
```

La base nacional de migración es material académico y presenta quiebres metodológicos, especialmente desde 2023. Las salidas municipales de movilidad y las departamentales de Sololá tienen alcances distintos. Este sistema no estima visitantes únicos del lago ni porcentajes de extranjeros. Las aclaraciones del catedrático sobre esos indicadores siguen pendientes.
