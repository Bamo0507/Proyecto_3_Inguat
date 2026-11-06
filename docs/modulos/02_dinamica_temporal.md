# **2. Modulo 2: Dinamica temporal, eventos y estimaciones**

**Estado.** Las vistas del módulo están implementadas. La comparación diaria usa los días regulares del mismo mes, municipio y procedencia. La serie mensual incorpora las estimaciones de enero y febrero de 2026 y el error de validación de mayo y junio de 2026.

**Lenguaje de la interfaz:** las preguntas de las tablas y de cada grafico son textos para el lector y usan lenguaje natural y ortografia completa. El titulo formula una pregunta concreta; municipio, fechas, unidad y base de comparacion se indican junto a la vista. Los terminos tecnicos necesarios se explican brevemente y las formulas se conservan en la documentacion metodologica. La redaccion sencilla no cambia la medida ni permite afirmar mas de lo que muestran los datos.

## **2.1. Proposito y preguntas**

Identificar cuando aumenta la presencia de visitantes en cada municipio, que diferencias se observan durante eventos y fines de semana, y que afluencia mensual se estima para enero-febrero de 2026.

Este modulo apoya la planificacion de fechas de mayor afluencia. Una mayor presencia no demuestra por si sola saturacion, dano ambiental ni efecto causal de una festividad. No se dispone de capacidad de carga ni de trayectorias individuales para sostener esas conclusiones.

Se trabajara un municipio y una procedencia a la vez. Nacionales y extranjeros conservaran analisis separados. La evolucion mensual observada del modulo 1 sirve de diagnostico; aqui el foco adicional es el detalle diario, los eventos, el patron semanal y la reconstruccion de los meses faltantes.

## **2.2. Correspondencia con el PDF**

Guia principal: `Guia_Proyecto_Observatorio_Turistico_UVG (1).pdf`, pagina 3. Referencia complementaria: [Guia de uso](../../data/raw/Guia_de_uso_de_los_datos_UVG.pdf), seccion 5.2, paginas 4-5.

| Contenido solicitado | Pregunta del lector | Representacion propuesta |
|---|---|---|
| Serie diaria y selector de eventos | ¿En qué fechas hubo más visitantes? | Linea diaria con dias del evento resaltados |
| Lift frente al dia regular promedio | ¿Cuánto cambiaron las visitas durante el evento? | Indicador porcentual junto a la linea, con base de comparacion visible |
| Patron por dia de semana | ¿Qué días de la semana reciben más visitantes? | Siete barras de promedio diario, de lunes a domingo |
| Estimacion obligatoria de enero-febrero de 2026 | ¿Cuántas visitas estimamos para enero y febrero de 2026? | Serie mensual observada con los dos meses estimados diferenciados |
| Validacion contra meses observados | ¿Cuánto se equivoca, en promedio, nuestra estimación? | MAE visible, con meses de validacion y unidad |

La interfaz contiene dos gráficos diarios y un gráfico mensual que responde a la procedencia seleccionada. El Lift y la validacion son lecturas asociadas a los graficos pertinentes, no motivos para agregar visualizaciones decorativas.

## **2.3. Fuentes y disponibilidad comprobada**

| Tabla procesada | Uso |
|---|---|
| `data/processed/movilidad_diaria/movilidad_diaria_atitlan.csv` | Presencia por dia, etiquetas de eventos y patron semanal |
| `data/processed/movilidad_mensual/movilidad_mensual_atitlan.csv` | Objetivo mensual de visitantes y validacion municipal |
| `data/processed/migracion/migracion_mensual.csv` | Referencia estacional de ingresos al pais |
| `data/processed/migracion/migracion_detalle.csv` | Consulta por mercado cuando sea necesaria para justificar la referencia estacional |
| `data/processed/dinamica_temporal/serie_municipal_mensual.csv` | Serie observada y estimada que se muestra en el módulo |
| `data/processed/dinamica_temporal/validacion_municipal.csv` | Error absoluto medio por municipio y procedencia |

La base diaria tiene diez meses completos: septiembre-diciembre de 2025 y marzo-agosto de 2026. Ademas tiene ventanas parciales en abril y junio de 2025 y septiembre de 2026. La comprobacion de fechas del archivo completo encontro que esas tres ventanas parciales no incluyen dias etiquetados `Regular`; la cobertura se volvera a comprobar para cada municipio y procedencia antes de calcular.

La movilidad mensual tiene diez meses observados; enero-febrero de 2026 no estan medidos. La migracion llega hasta junio de 2026, mientras la movilidad mensual llega hasta agosto: hay ocho meses calendario coincidentes entre ambas para calibraciones que requieran sus valores observados. No se supondra que existen datos migratorios de julio-agosto en el paquete.

Las fechas y los municipios deben relacionarse por dimensiones comunes. La escritura distinta de un municipio entre tablas no constituye un destino distinto ni debe dejar un cruce vacio.

## **2.4. Filtros y alcance propuestos**

| Control | Alcance | Comportamiento |
|---|---|---|
| Municipio | Todo el modulo | Actualiza las vistas y selecciona la estimacion y validacion de ese municipio |
| Nacionales / extranjeros | Todo el módulo | Selecciona la procedencia de la vista diaria, del patrón semanal y de la serie mensual |
| Mes y anio | Bloque diario y semanal | Muestra los dias observados del mes, su cobertura y el patron semanal correspondiente |
| Evento | Local a la linea diaria y su Lift | Resalta los dias del evento en el mes; conserva los dias de contexto para comparar |

El bloque de estimacion mensual conserva su ventana completa, con enero-febrero destacados. No cambia ni vuelve a entrenar el modelo al seleccionar un evento o un mes del bloque diario. La metrica de validacion tampoco se recalcula con filtros que no pertenecen a su protocolo.

El selector de evento solo ofrece etiquetas presentes en la seleccion. Si no hay festividades, la serie sigue siendo util y se informa que no hay un evento registrado para comparar. Seleccionar una festividad no filtra silenciosamente la base de dias regulares ni cambia el grafico semanal para que represente solo esa fiesta.

No se agregan filtros por pais, semana ISO, rango diario libre ni algoritmo en esta primera version. Los filtros de municipio, mes y evento permiten buscar entre sus opciones. Mes y evento se ubican junto a la vista diaria.

## **2.5. Graficos y medidas**

### **2.5.1. Visitas por dia y eventos**

Pregunta: "¿En qué fechas hubo más visitantes?".

- Eje horizontal: fecha diaria real, en orden cronologico.
- Eje vertical: presencia diaria reportada del municipio y procedencia.
- Primero sumar los paises identificados dentro del mismo dia y universo, luego representar cada dia. No calcular una media entre filas de paises como si fueran dias.
- Resaltar las fechas etiquetadas con el evento seleccionado y conservar el contexto de dias regulares. El titulo identifica mes, municipio y procedencia.
- Una linea de referencia puede mostrar el promedio de dias regulares del mismo mes, cuando exista una base valida.
- Las ventanas parciales deben identificarse como tales. No unir fechas ausentes ni completar con ceros.
- La suma de presencias diarias no se presentara como visitantes unicos del mes.

**Lift o variacion frente a dias regulares:**

Pregunta: "¿Cuánto cambiaron las visitas durante el evento?". La aclaracion visible sera "Comparado con el promedio diario de los días sin eventos registrados". Se comparan promedios por dia, no acumulados de ventanas de distinta duracion.

`100 * (promedio de presencia por dia del evento / promedio de presencia por dia regular - 1)`.

Ambos promedios se calculan sobre dias observados del mismo municipio, mes y procedencia, mostrando la cantidad de dias de cada grupo. La lectura visible utilizara lenguaje como "Variacion frente a dias regulares" y explicara la referencia; un aumento no se califica automaticamente como positivo.

Si no hay dias regulares, dias del evento o una referencia positiva, no se calcula el porcentaje. Se muestra "Sin referencia comparable" o "Sin dato", segun corresponda. No se toma automaticamente otro mes o anio para fabricar la comparacion. Otra referencia debera justificarse en el analisis antes de incorporarla.

El Lift es una comparacion descriptiva. Puede reflejar diferencias de temporada o composicion de dias de semana; no demuestra que el evento causo el cambio. Las etiquetas se usan como ventanas de la fuente, sin afirmar que la festividad ocurrio localmente en todos los municipios.

### **2.5.2. Visitas por dia de la semana**

Pregunta: "¿Qué días de la semana reciben más visitantes?".

- Siete barras en orden lunes-domingo, con eje de cantidades desde cero y valores visibles.
- Utilizar presencia diaria promedio, no totales acumulados por dia de semana: un mes puede contener distintas cantidades de lunes y domingos.
- Propuesta: construir el patron habitual con dias `Regular`, para distinguirlo del analisis especifico de eventos. Identificar esta exclusion en el titulo o subtitulo.
- Calcular sobre los totales diarios ya agregados por municipio y procedencia. Informar cuantos dias observados sustentan cada promedio.
- Resaltar sabado y domingo con un acento consistente, sin asignar siete colores distintos.
- Si falta una categoria de dia, mostrar sin dato, no cero. Si la seleccion solo contiene una ventana de evento, informar que no hay base regular para un patron habitual.
- No anadir un KPI de fin de semana salvo que el analisis posterior demuestre su utilidad; las siete barras ya permiten responder la pregunta.

### **2.5.3. Estimacion de enero-febrero de 2026**

Pregunta: "¿Cuántas visitas estimamos para enero y febrero de 2026?".

- Serie mensual para el municipio y procedencia, con medidas observadas y los dos meses estimados.
- Identificar enero-febrero con rotulo `Estimacion`, estilo de linea o marcador distinto y color diferenciado del observado. No depender exclusivamente del color.
- Meses y anios en el eje horizontal; visitantes mensuales en el vertical. Los valores de enero y febrero deben poder leerse sin hover.
- Incluir incertidumbre si el metodo produce un intervalo defendible y explicar su significado. No inventar bandas usando una metrica global de error.
- Esta es una estimacion de dos meses faltantes dentro del periodo, no una proyeccion indefinida del turismo ni una prediccion de hoteleria.

**Tratamiento metodologico que debe resolverse en el analisis:**

- Construir una referencia estacional de migracion y un factor de reparto o calibracion a partir de movilidad observada, por municipio y procedencia. No asignar a todos los municipios una misma curva sin justificar su ajuste local.
- El factor ajusta universos de medicion diferentes; no debe rotularse automaticamente como porcentaje real de todas las personas que ingresan al pais y visitan el municipio.
- La migracion mide ingresos al pais y no desplazamientos internos de residentes. Su uso para nacionales es una aproximacion que requiere declarar el supuesto y revisar su error por separado.
- Respetar el quiebre metodologico migratorio de 2023. Las ventanas del laboratorio nacional previo no son por si mismas validacion de Atitlan.
- Elegir el metodo por su validez y error sobre el objetivo municipal; no trasladar automaticamente el SARIMA nacional ni todos los modelos anteriores.
- Usar la base diaria como comprobacion de la forma intramensual en fechas coincidentes, segun la guia. No sumar sus presencias ni equipararlas con el nivel mensual de visitantes unicos. No proyectar la serie diaria.

**Validacion y metrica propuesta:**

Pregunta: "¿Cuánto se equivoca, en promedio, nuestra estimación?". La vista indicara que se comprobo estimando meses cuyos datos ya se conocen y expresara el error en visitantes por mes.

- Ocultar meses realmente observados y estimarlos sin usar sus valores objetivo para ajustar ni el modelo ni el factor de reparto.
- Evaluar el procedimiento completo de estimacion municipal, no solo la serie nacional de migracion.
- Registrar meses usados para ajustar y evaluar, numero de observaciones y criterio de separacion adecuado a una reconstruccion retrospectiva. No presentar el ejercicio como pronostico disponible antes de la fecha si utilizo informacion posterior.
- Reportar MAE, admitido por la guia: promedio del valor absoluto de la diferencia entre estimacion y observacion. Expresarlo en visitantes por mes, para el municipio y procedencia evaluados.
- No calcular el error de enero-febrero frente a una verdad no disponible. La metrica proviene de los meses observados reservados para validacion.
- Declarar la limitacion de una validacion con pocos meses. Un error elevado se informa; no se oculta ni se cambia de metrica solo para mejorar la apariencia.

## **2.6. Criterios comunes y limites**

- No sumar municipios ni mezclar cantidades nacionales y extranjeras.
- No asignar paises nulos a un grupo de procedencia. Informar su exclusion cuando afecte la seleccion.
- Mantener dias sin cobertura, ceros observados, falta de referencia y errores como estados distintos.
- Fuente, cobertura, universo, unidad y filtros deben ser legibles. La informacion principal no depende de un tooltip ni de explicacion oral.
- Las cantidades y promedios mantienen su precision durante el calculo; el formato se aplica al presentar.
- No incluir en esta fase mapas, pruebas de multiples algoritmos en la interfaz, pronosticos hoteleros ni proyecciones diarias.

## **2.7. Resultado de la propuesta**

Los gráficos diarios y la serie mensual de la procedencia seleccionada cubren las preguntas del módulo. La variación de cada evento se muestra cuando hay una referencia regular comparable. La regresión lineal usa el mes y los ingresos migratorios para estimar los dos meses faltantes. El error se informa por municipio y procedencia con los dos meses observados que se reservaron para la validación.
