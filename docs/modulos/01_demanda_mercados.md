# **1. Modulo 1: Demanda y mercados emisores**

**Estado:** definicion funcional aprobada al cerrar la revision consolidada del modulo. El documento orienta la futura implementacion de indicadores, graficos y filtros.

**Lenguaje de la interfaz:** las preguntas de las tablas y de cada grafico son textos para el lector y usan lenguaje natural y ortografia completa. El titulo formula una pregunta concreta; municipio, fechas, unidad y base de comparacion se indican junto a la vista. Los terminos tecnicos necesarios se explican brevemente y las formulas se conservan en la documentacion metodologica. La redaccion sencilla no cambia la medida ni permite afirmar mas de lo que muestran los datos.

## **1.1. Proposito y alcance**

Responder quien llega al municipio seleccionado, cuanto volumen de visitas registra, cuanto permanece y de que paises procede. La lectura debe ser rapida para una persona no tecnica, con titulos naturales, unidades, municipio y periodo visibles.

Este modulo describe un municipio a la vez. La comparacion detallada y simultanea de los diez municipios pertenece al modulo 4. La evolucion diaria, los eventos y las estimaciones de enero-febrero corresponden al modulo 2. La comparativa de afluencia requerida en el modulo 3 se coordinara con el reto territorial sin duplicar graficos sin una pregunta distinta.

## **1.2. Cobertura de lo solicitado en el PDF**

Referencia principal: `Guia_Proyecto_Observatorio_Turistico_UVG (1).pdf`, pagina 3, "Modulos obligatorios". Referencia metodologica: [Guia de uso de los datos](../../data/raw/Guia_de_uso_de_los_datos_UVG.pdf), seccion 5.1, pagina 4.

| Requisito | Pregunta del lector | Elemento previsto | Cobertura |
|---|---|---|---|
| Visitantes promedio por mes | ¿Cuántas visitas recibe este municipio en promedio por mes? | KPI de promedio mensual observado | Requisito cubierto, adaptado a municipio |
| Dias-persona | ¿Cuántos días de visita se registraron en total este mes? | KPI de dias-persona del mes | Requisito cubierto |
| Estadia media ponderada, solo mayor a un dia | ¿Cuántos días se quedan, en promedio, quienes pasan la noche? | KPI de estadia media del mes | Formula y periodo mensual acordados |
| Proporcion de visitas con pernocta y de paso | ¿Hay más visitas de paso o de personas que se quedan a dormir? | Dos barras horizontales al 100 %, nacionales y extranjeros separados | Requisito cubierto |
| Diez principales mercados emisores | ¿De qué países vienen más visitantes extranjeros? | Top 10 con barras horizontales ordenadas | Requisito cubierto; nacionales tratados en su propio segmento |
| Visualizacion adicional pertinente | ¿Cómo cambia el número de visitas de un mes a otro? | Linea mensual observada con huecos de cobertura | Adicion aprobada; no requiere ampliar el alcance |

No se necesita un grafico independiente por cada KPI ni incorporar otra fuente para cubrir este modulo. La linea observada es el unico grafico adicional previsto.

## **1.3. Aclaraciones autorizadas y base disponible**

Segun la respuesta del catedratico comunicada por Bryan:

- Se adaptaran los indicadores a los datos municipales disponibles; no se exige fabricar un total unico del lago ni una base poblacional inexistente.
- Nacionales y extranjeros se analizaran por separado porque se desconocen los ajustes que recibieron sus cantidades.

Fuente: `BD_moviidad_mensual.xlsx`, hoja `Atitlan`. Tabla procesada: `data/processed/movilidad_mensual/movilidad_mensual_atitlan.csv`.

La comprobacion de disponibilidad confirma diez municipios y diez meses observados para cada municipio y segmento de procedencia: septiembre-diciembre de 2025 y marzo-agosto de 2026. Existen registros de ambas categorias de permanencia en cada combinacion municipio-mes-procedencia. Hay al menos diez paises extranjeros identificados para cada municipio y mes. Estas comprobaciones respaldan la viabilidad de las vistas; no equivalen a conclusiones sobre preferencias turisticas.

Enero-febrero de 2026 no tienen observaciones. La limpieza no los convierte en ceros, y este modulo mostrara solo datos observados.

## **1.4. Filtros y actualizacion acordados**

### **1.4.1. Controles**

| Control | Alcance | Comportamiento |
|---|---|---|
| Municipio | General | Actualiza las medidas y vistas del municipio |
| Mes y anio en un unico selector | General | Actualiza los resultados mensuales; mantiene la cobertura completa de la linea y resalta el mes elegido |
| Nacionales / extranjeros | Local al bloque de KPIs y linea | Cambia ese bloque entre universos separados, sin sumarlos |

El selector de procedencia debe estar ubicado y rotulado dentro del bloque que controla. No sera un filtro general que haga desaparecer el ranking extranjero o contradiga las dos barras de composicion.

El ranking se identificara siempre como **paises extranjeros**. Las dos barras de proporcion conservaran nacionales y extranjeros en filas separadas, cada una con su propia base del 100 %. Ambas vistas reciben municipio y mes, no el selector local de procedencia.

No se incorporaran rangos multimes, un filtro independiente de anio, filtros por pais o filtros de permanencia en esta primera version. El ranking no funcionara como un filtro oculto al hacer clic. La lectura inicial debe estar poblada con un municipio y un mes observados, visibles en los selectores; el valor inicial concreto puede resolverse al implementar.

### **1.4.2. Que cambia con cada seleccion**

| Elemento | Cambiar municipio | Cambiar mes | Cambiar procedencia local |
|---|---|---|---|
| Promedio mensual | Recalcula | Mantiene la referencia del periodo observado | Recalcula |
| Dias-persona | Recalcula | Recalcula | Recalcula |
| Estadia media mensual | Recalcula | Recalcula | Recalcula |
| Evolucion mensual | Cambia la serie | Conserva la serie y cambia el mes resaltado | Cambia la serie |
| Top 10 extranjero | Recalcula | Recalcula | No cambia: universo extranjero explicito |
| Dos barras de pernocta/paso | Recalcula | Recalcula | No cambian: muestran ambos segmentos |

La referencia del periodo completo se distinguira de los resultados del mes, con el periodo escrito junto a cada medida. No se mostraran datos de la seleccion anterior bajo etiquetas nuevas durante una actualizacion.

La linea, el ranking y las barras de composicion quedan vinculados por municipio y mes. Esto permite desarrollar tres visualizaciones coordinadas, conforme al criterio de interactividad de la guia principal, sin agregar controles por grafico.

## **1.5. Indicadores y graficos**

### **1.5.1. Tres indicadores principales**

**Promedio mensual de visitas: aprobado como referencia general.**

Pregunta: "¿Cuántas visitas recibe este municipio en promedio por mes?".

- Suma de visitantes de los meses observados incluidos, dividida entre el numero de esos meses, para un municipio y una procedencia.
- En la fuente actual se utilizan diez meses observados. Enero y febrero no entran como ceros en el denominador.
- Debe indicar cobertura y numero de meses. Cambiar solo el mes de detalle no transforma este KPI en la cantidad de ese mes.
- La suma intermedia no se publica como personas unicas del periodo completo.

**Dias-persona del mes: aprobado.**

Pregunta: "¿Cuántos días de visita se registraron en total este mes?". La unidad sigue siendo dias-persona; se explica mediante el ejemplo de visitantes y dias de permanencia, sin cambiar el calculo.

- Suma de `dias_persona` para municipio, mes y procedencia, conservando las categorias de permanencia disponibles.
- Mes, anio y unidad visibles. Una explicacion breve puede ilustrar que diez visitantes con tres dias de permanencia representan treinta dias-persona; ese ejemplo no es un resultado del proyecto.
- Esta medida utiliza el significado reportado por la fuente, incluida la convencion de permanencia de los visitantes de paso; no se rotulara como noches de hotel.

**Estadia media del mes: aprobada en la revision consolidada.**

Pregunta: "¿Cuántos días se quedan, en promedio, quienes pasan la noche?".

- Suma de `dias_persona` dividida entre suma de `visitantes`, solo para `es_consecutivo = mayor a 1 dia`, dentro del municipio, mes y procedencia.
- Unidad: dias por visitante del segmento con pernocta. No se promedia `permanencia_prom` ni se incluyen visitas de paso en este cociente.
- Un denominador cero produce una medida no definida.

Se reutilizara el diseno de KPI aprobado: tarjeta clara, cifra azul, icono discreto y contexto integrado, sin pie separado ni divisor horizontal. No se agregaran variaciones, metas o tendencias pequenas sin una comparacion valida y una necesidad concreta.

### **1.5.2. Top 10 de paises extranjeros: aprobado**

- Pregunta: "¿De qué países vienen más visitantes extranjeros?".
- Barras horizontales, pais en el eje vertical y visitantes del mes en el horizontal desde cero. Orden descendente y cantidades visibles al final de las barras.
- Sumar los registros de las dos categorias de permanencia dentro de cada pais, municipio y mes. No sumar municipios ni meses.
- Usar todos los paises extranjeros identificados para calcular el ranking, seleccionar diez y excluir Guatemala y paises no identificados.
- Regla operativa recomendada para empates: ordenar por cantidad sin redondear y, en igualdad exacta, por nombre de pais, manteniendo un maximo de diez entradas.
- Un solo color de la paleta del proyecto. No se necesita un color por pais ni un mapa para comparar este ranking.
- El titulo o subtitulo identificara municipio y mes. No presentar el Top 10 como si fuera toda la poblacion extranjera.

### **1.5.3. Visitas de paso y con pernocta: aprobado**

- Pregunta: "¿Hay más visitas de paso o de personas que se quedan a dormir?".
- Dos barras horizontales apiladas al 100 %, una para nacionales y otra para extranjeros. Cada barra tiene su propio denominador y se divide entre las dos categorias originales de permanencia.
- Porcentaje de cada categoria: visitantes de esa categoria divididos entre visitantes de las dos categorias del mismo municipio, mes y procedencia.
- El universo extranjero incluye todos los paises extranjeros identificados, no solo el Top 10.
- Mostrar categorias y porcentajes con etiquetas directas; colocar fuera el texto que no quepa dentro de un tramo. Dos colores distinguibles y consistentes, con texto como segundo canal.
- La vista describe la composicion interna de cada universo. No representa participacion extranjera sobre nacionales ni permite deducir la relacion entre sus cantidades absolutas.

### **1.5.4. Evolucion mensual observada: aprobado**

- Pregunta: "¿Cómo cambia el número de visitas de un mes a otro?".
- Linea con meses y anios reales en orden cronologico; visitantes del municipio y procedencia en el eje vertical.
- Mantener la serie observada completa al elegir un mes, resaltando el punto correspondiente. La cantidad de ese mes debe ser legible sin depender exclusivamente del tooltip.
- Dejar un hueco en enero-febrero de 2026 y no conectar ambos tramos como si hubiera mediciones continuas.
- No incluir aqui las estimaciones ni presentar comparaciones interanuales, porque no hay un mismo mes observado en ambos anios.
- La vista describe el comportamiento disponible, no demuestra por si sola una estacionalidad anual estable. El modulo 2 desarrolla dias, eventos y estimaciones.

## **1.6. Reglas comunes y control de calidad**

- No sumar municipios para fabricar visitantes unicos del lago ni nacionales y extranjeros para construir un total combinado.
- No sumar presencias diarias para obtener visitantes mensuales.
- Mantener la clasificacion original de permanencia, incluso si el cociente de una fila da uno.
- No asignar paises nulos a nacionales o extranjeros. Mantenerlos como `Pais no identificado` en una nota de cobertura cuando afecten la seleccion, sin agregarlos como pais ficticio al ranking.
- Distinguir una medicion de cero, una proporcion no definida, un periodo sin cobertura, una carga y un error.
- Mantener la precision para calcular, ordenar y obtener proporciones. El redondeo de presentacion de visitantes se aplica al final; el orden no se calcula sobre cifras ya redondeadas.
- Identificar fuente, cobertura, unidad y segmento. La informacion indispensable no queda escondida en hover.
- Antes de publicar, comprobar etiquetas, contraste, colores distinguibles y lectura al tamano pertinente al producto. No anadir variedad grafica sin significado.

## **1.7. Resultado de la revision**

El alcance propuesto cubre todos los contenidos obligatorios del modulo 1 con **tres tipos de KPI y tres visualizaciones**. El total del lago y la participacion extranjera sobre un universo combinado se sustituyen por el tratamiento municipal y separado autorizado por el catedratico.

La coordinacion de filtros y la estadia del mes quedaron aprobadas al cerrar la revision conjunta. Las reglas menores de empates y los valores iniciales no necesitan convertirse en nuevas rondas de discusion. La relacion adicional entre volumen y estadia por mercado no se incluye en esta primera version, porque no es necesaria para responder el alcance acordado.
