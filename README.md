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

## Organizacion por etapas

Cada archivo numerado contiene la transformacion de su fuente. `run_pipeline.py` solo ejecuta esas etapas en orden y se detiene ante un error de contrato; `config.py` concentra rutas y esquemas, y `utils.py` comparte lectura, escritura y validaciones.

```text
data/raw/
    |
    +-- movilidad_mensual/diaria: ingesta -> seleccion -> normalizacion -> tipado
    +-- migracion:               ingesta -> seleccion -> normalizacion -> tipado -> mensual
    +-- ocupacion/oferta:        ingesta -> seleccion -> tipado
    |
    v
data/processed/<fuente>/
    +-- NN_<etapa>.csv          intermedios auditables
    +-- <tabla_final>.csv       salidas analiticas
    +-- incidencias*.csv        evidencia de reparaciones y rechazos
    +-- informe_ejecucion.json  huella del original y lista de salidas
```

| Fuente | Archivo en su directorio de `src/` | Responsabilidad | Entrada | Salida |
|---|---|---|---|---|
| Las cinco | `01_ingesta.py` | Lectura fiel del original | `data/raw/<archivo>` | `01_ingesta.csv` |
| Las cinco | `02_seleccion.py` | Poblacion y columnas acordadas | `01_ingesta.csv` | `02_seleccion.csv` |
| Movilidad mensual, diaria y migracion | `03_normalizacion.py` | Reparaciones de categorias documentadas | `02_seleccion.csv` | `03_normalizacion.csv` |
| Movilidad mensual, diaria y migracion | `04_tipado.py` | Tipos y contrato final | `03_normalizacion.csv` | `04_tipado.csv` y tabla final |
| Ocupacion y oferta | `03_tipado.py` | Tipos y rechazo documentado de cantidades invalidas | `02_seleccion.csv` | `03_tipado.csv`, tabla final e `incidencias_tipado.csv` |
| Migracion | `05_mensual.py` | Serie mensual y ventanas historicas | `04_tipado.csv` | `05_mensual.csv` y series finales |

Esta separacion permite revisar y volver a ejecutar una etapa sin mezclar las reglas de los cinco libros en una funcion central.

En ocupacion y oferta, una cantidad ausente o invalida conserva su fila y pasa a nulo. `incidencias_tipado.csv` registra `fila_csv` (cabecera = fila 1), columna, valor original, valor de salida, motivo y clasificacion. Las ausencias se distinguen de los rechazos por invalidez. Una inconsistencia entre cantidades de capacidad se senala como `requiere_revision`, conservando las cantidades: no se puede deducir cual corregir. Una fecha, clave o cobertura invalida sigue deteniendo el proceso. Con los originales actuales, estos dos informes no contienen incidencias y conservan sus cabeceras.

## Verificación

```bash
.venv/bin/python -m unittest discover -s tests -v
```

La base nacional de migración es material académico y presenta quiebres metodológicos, especialmente desde 2023. Las salidas municipales de movilidad y las departamentales de Sololá tienen alcances distintos. Este sistema no estima visitantes únicos del lago ni porcentajes de extranjeros. Las aclaraciones del catedrático sobre esos indicadores siguen pendientes.
