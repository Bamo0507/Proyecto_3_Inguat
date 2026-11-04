# Diccionario de tablas finales

Todas las tablas se guardan en `data/processed/<fuente>/`. Formato CSV UTF-8; nulo `\N`; decimales exactos del origen o suma decimal; fechas ISO. Los nombres de columnas son `snake_case` sin tildes. Las categorías conservan su escritura de la fuente salvo reparaciones descritas.

## `movilidad_mensual/movilidad_mensual_atitlan.csv`

9,860 filas; municipios del lago; septiembre–diciembre de 2025 y marzo–agosto de 2026. Clave: `destino, fecha, pais, es_consecutivo`.

| Columna | Tipo y unidad | Regla |
|---|---|---|
| `destino` | texto, municipio | 10 municipios del lago. |
| `anio` | entero, año calendario | Coherente con fecha. |
| `mes` | entero, 1–12 | Coherente con fecha. |
| `pais` | texto o nulo, residencia | 13 vacíos y 12 `Null` pasan a nulo; conserva filas. |
| `es_consecutivo` | texto, grupo de permanencia | Conserva `menor a 1 dia` y `mayor a 1 dia`. |
| `fecha` | fecha y hora, inicio de mes | `AAAA-MM-DD 00:00:00`. |
| `visitantes` | decimal no negativo, visitantes reportados | Conserva ceros y precisión. |
| `dias_persona` | decimal no negativo, días persona | Conserva ceros y precisión. |

Se retiran `sub_grupo` (constante) y `permanencia_prom` (derivable). Los 778 registros de `mayor a 1 dia` con promedio uno no se reclasifican. Un cociente con denominador cero queda indefinido si se calcula después. Enero y febrero de 2026 no tienen observaciones en esta fuente. No se suman municipios para fabricar visitantes únicos.

## `movilidad_diaria/movilidad_diaria_atitlan.csv`

82,952 filas; 10 municipios; ventanas observadas entre abril de 2025 y septiembre de 2026. Clave: `destino, idfecha, pais`.

| Columna | Tipo y unidad | Regla |
|---|---|---|
| `destino` | texto, municipio | Etiqueta original. |
| `anio`, `mes` | enteros, calendario | Coherentes con `idfecha`. |
| `idfecha` | fecha y hora | `AAAA-MM-DD HH:MM:SS`. |
| `dia_semana` | texto | Coherente con la fecha; escritura original. |
| `pais` | texto o nulo | 28 vacíos y 13 `NULL` pasan a nulo; `ESPAÃ±A` pasa a `ESPAÑA` en 1,376 filas. |
| `num_semana` | entero, semana ISO 1–53 | Renombre de `Week`; el año ISO puede diferir del calendario. |
| `evento` | texto | Etiqueta original, incluida `Regular`. |
| `cantidad_visitantes` | decimal no negativo, presencias diarias | Conserva ceros y precisión. |

Se retira `sub_grupo`. Las ventanas parciales no se completan; enero y febrero de 2026 carecen de observaciones. Las presencias diarias no son visitantes únicos mensuales.

## `migracion/migracion_detalle.csv`

132,894 filas de `Turista` y `Excursionista` sin residencia `Guatemala`, desde enero de 2009 a junio de 2026. Parte de 161,036 filas de origen; 137,642 tras seleccionar tipos y 132,894 tras excluir 4,748 residentes. La clave original completa incluye año, mes, vía, frontera, país, tipo y agrupación de residencia. Tras normalizar se permiten 40 filas en 20 claves compartidas conocidas, conservando ambas filas y sus cantidades; `incidencias.csv` registra su fila Excel.

| Columna | Tipo y unidad | Regla |
|---|---|---|
| `anio`, `mes` | enteros, calendario | 2009–2026 y 1–12. |
| `via` | texto | Según código de frontera conocido; 92 reparaciones en la población seleccionada (93 en origen completo). |
| `frontera` | texto | Código y nombre originales. |
| `pais` | texto o nulo | Primera forma registrada para variantes solo de mayúsculas; puede ser un mercado agrupado desde 2023. |
| `region`, `region_dos`, `regiones_omt`, `mceo` | texto o nulo | Catálogos diferentes. `0` en `region_dos` y `0x2a` en `regiones_omt` se rechazan a nulo. |
| `agrupacion_residencia` | texto o nulo | `Resto de mundo` → `Resto del Mundo`. |
| `tipo_viajero` | texto | `Turista` o `Excursionista`; distinto de la medida `viajeros`. |
| `viajeros` | decimal no negativo, ingresos reportados | Ceros y decimales conservados. |
| `fecha` | fecha, primer día del mes | `AAAA-MM-DD`. |

La hoja `Notas` del libro describe uso académico, cambios de fuente en 2021 y 2023 y mercados agrupados desde 2023. Se conserva la ingesta completa como `01_ingesta.csv`; el detalle final es la vista analítica filtrada. `SIN ESPECIFICAR` sigue siendo una categoría explícita.

### `migracion/migracion_mensual.csv`

210 meses en rejilla de enero de 2009 a junio de 2026. Clave: `fecha`.

| Columna | Tipo y unidad | Regla |
|---|---|---|
| `fecha` | fecha mensual | Primer día del mes. |
| `viajeros` | decimal o nulo, ingresos nacionales | Suma de detalle; abril–agosto de 2020 son nulos porque no hay registros de la población objetivo. |
| `registros` | entero, filas agregadas | Cero cuando no hay filas; no es cantidad de personas. |
| `conjunto` | texto | `historico`, `ajuste` o `evaluacion`. |

`migracion_ajuste_2023_2025.csv` contiene 36 meses y `migracion_evaluacion_2026_01_06.csv` seis meses. Son ventanas históricas para una evaluación futura; no son predicciones ni entrenamiento.

## `ocupacion_hotelera/ocupacion_solola.csv`

36 meses completos, enero de 2023 a diciembre de 2025; departamento Sololá. Clave: `fecha`.

| Columna | Tipo y unidad | Regla |
|---|---|---|
| `fecha` | fecha mensual `AAAA-MM-DD` | Primer día del mes derivado de año y mes. |
| `indice_ocupacion` | decimal, proporción de 0 a 1 | Escala original; no multiplicar por cien. |

Se filtra `Sololá` y se retiran año, mes y departamento después de validar. Los extremos respaldados por boletines se conservan.

## `oferta_alojamiento/oferta_solola.csv`

15 filas: tres tipos por cinco cortes de Sololá. Clave: `anio, trimestre, tipo_alojamiento`.

| Columna | Tipo y unidad | Regla |
|---|---|---|
| `anio` | entero, año del corte | 2022–2026. |
| `trimestre` | entero, trimestre del corte | Cuarto trimestre 2022–2025; primero de 2026. |
| `tipo_alojamiento` | texto | `Hospedaje`, `Hotel`, `Pensión`. |
| `establecimientos` | entero no negativo, establecimientos | Inventario registrado. |
| `habitaciones` | entero no negativo, habitaciones | Inventario registrado. |
| `plazas_cama` | entero no negativo, plazas | Capacidad de personas. |

Se filtra `Sololá` y se retira departamento. Los inventarios repetidos entre años se conservan. El corte de 2026 es parcial y no equivale a un cierre anual. No se inventan fechas diarias ni trimestres ausentes.
