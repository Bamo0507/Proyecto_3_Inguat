# **3. Modulo 3: Oferta hotelera y desagregacion territorial**

**Estado:** alcance funcional aprobado tras la revision conjunta, incluida la aclaracion visible de la ventana septiembre-diciembre de 2025. No se han implementado indicadores ni graficos.

**Lenguaje de la interfaz:** las preguntas de las tablas y de cada grafico son textos para el lector y usan lenguaje natural y ortografia completa. El titulo formula una pregunta concreta; municipio, fechas, unidad y base de comparacion se indican junto a la vista. Los terminos tecnicos necesarios se explican brevemente y las formulas se conservan en la documentacion metodologica. La redaccion sencilla no cambia la medida ni permite afirmar mas de lo que muestran los datos.

## **3.1. Proposito y limites territoriales**

Describir la capacidad registrada de alojamiento de Solola, su ocupacion y el contexto de afluencia de los municipios del lago. El modulo debe distinguir de forma visible las dos escalas: oferta y ocupacion son departamentales; la movilidad es municipal.

La comparacion de afluencia entre municipios es un requisito propio de este modulo. El modulo 4 profundizara en sus perfiles y en el cruce de volumen con estadia; no se trasladara todo el requisito territorial al cuarto modulo ni se sumaran municipios para fabricar un total del lago.

## **3.2. Correspondencia con las instrucciones**

Referencia principal: `Guia_Proyecto_Observatorio_Turistico_UVG (1).pdf`, pagina 3. Referencia complementaria: [Guia de uso](../../data/raw/Guia_de_uso_de_los_datos_UVG.pdf), seccion 5.3, pagina 5.

| Requisito | Pregunta del lector | Representacion propuesta |
|---|---|---|
| Capacidad de alojamiento de 2022-2025 | ¿Cómo ha cambiado la capacidad de alojamiento de Sololá? | Tres pequenos graficos de barras por corte anual, uno por medida |
| Ocupacion mensual de 2023-2025 | ¿Qué porcentaje de las habitaciones disponibles estuvo ocupado cada mes? | Linea mensual continua en porcentaje |
| Cruce afluencia-ocupacion, septiembre-diciembre de 2025 | ¿Cómo cambiaron las visitas al municipio y la ocupación hotelera de Sololá? | Dos paneles alineados por mes, con unidades separadas |
| Comparacion entre subdestinos | ¿Qué municipios recibieron más visitas este mes? | Barras horizontales de los diez municipios, sin porcentajes de participacion sobre un total del lago |

Se proponen cuatro bloques analiticos. No se agregan pronosticos hoteleros, mapas ni mas indicadores por defecto. La primera vista contiene tres medidas porque son las tres solicitadas, no porque exista una necesidad de multiplicar paneles.

## **3.3. Fuentes y cobertura comprobada**

- `data/processed/oferta_alojamiento/oferta_solola.csv`: quince filas, tres tipos de alojamiento por cinco cortes. Los cortes de 2022-2025 son del cuarto trimestre; 2026 corresponde al primero y es parcial.
- `data/processed/ocupacion_hotelera/ocupacion_solola.csv`: 36 meses, enero de 2023 a diciembre de 2025, con `fecha` e `indice_ocupacion`.
- `data/processed/movilidad_mensual/movilidad_mensual_atitlan.csv`: afluencia por municipio y procedencia. El cruce con ocupacion se limita a septiembre-diciembre de 2025.

Los datos hoteleros no permiten distribuir inventario u ocupacion entre municipios, separar huespedes por nacionalidad ni identificar alojamientos individuales. Tampoco incluyen automaticamente plataformas digitales.

Se conserva como nota metodologica el rotulo `Solola, Panajachel` de los boletines de 2023 y 2024. El CSV se trabaja como Solola; ese rotulo no autoriza a presentar la ocupacion como dato exclusivo de Panajachel.

## **3.4. Controles locales y actualizacion**

La interfaz debe separar un bloque departamental de inventario/ocupacion de otro bloque de movilidad y cruce. Un filtro municipal no debe cambiar el alcance de una cifra departamental.

| Control | Afecta | No modifica |
|---|---|---|
| Tipo de alojamiento: todos, hotel, hospedaje o pension | Los tres graficos de inventario | La ocupacion, porque la tabla no tiene desglose por tipo, ni las visitas municipales |
| Municipio | La serie municipal del cruce y el resaltado del municipio en el ranking | Inventario y ocupacion de Solola; el ranking conserva los diez municipios |
| Nacionales / extranjeros | La afluencia usada en el cruce y en el ranking | Oferta y ocupacion departamentales |
| Mes: septiembre-diciembre de 2025 | Ranking municipal y resaltado de ese mes en el cruce y la ocupacion | Inventario anual y ventanas completas de las series |

El selector de mes estara ubicado en el bloque de movilidad y cruce. Solo ofrece la ventana coincidente en esta primera version. La comparacion territorial de todos los meses observados queda disponible en el modulo 4.

La ocupacion mantiene visibles sus 36 meses. El panel de cruce mantiene visibles los cuatro meses coincidentes, sin reducirse a un punto al seleccionar un mes. El ranking conserva todas las filas y resalta el municipio elegido; no se filtra hasta dejar una sola barra.

No se necesita un filtro general de anio, trimestre o pais. Los controles de una fuente no se aplican a otra que no contiene ese desglose.

## **3.5. Definicion de las visualizaciones**

### **3.5.1. Capacidad de alojamiento de Solola**

Pregunta: "¿Cómo ha cambiado la capacidad de alojamiento de Sololá?".

Las tres medidas se explicaran como alojamientos registrados, habitaciones y personas que pueden hospedarse al mismo tiempo. La ultima corresponde a plazas-cama; no a camas fisicas ni a huespedes efectivamente recibidos.

- Tres graficos de barras pequenos y alineados, con 2022, 2023, 2024 y 2025 en orden cronologico.
- Cada medida conserva su propio eje desde cero y sus unidades: establecimientos, habitaciones o plazas de personas. No se mezclan las tres cantidades en un mismo eje como si fueran la misma medida.
- Cantidades visibles sobre las barras y etiqueta de cuarto trimestre. Se representan inventarios, no un flujo acumulado ni una tendencia modelada.
- Con `Todos` se suman los tres tipos dentro del mismo corte. Al elegir un tipo, se actualizan las tres medidas para esa categoria.
- No se suman cortes de anios distintos ni se rellenan trimestres intermedios. No se ajustan lineas de tendencia o estacionalidad a cuatro o cinco observaciones.
- La vista principal usa 2022-2025. El corte de 2026 se conserva como informacion adicional separada, rotulada "Inventario parcial del primer trimestre de 2026; no comparable directamente con los cierres anteriores", sin tasa de crecimiento frente a 2025.

### **3.5.2. Ocupacion departamental**

Pregunta: "¿Qué porcentaje de las habitaciones disponibles estuvo ocupado cada mes?".

- Linea de enero de 2023 a diciembre de 2025, ordenada por fecha.
- Eje vertical porcentual con rango de 0 a 100 %. La columna conserva su proporcion original; por ejemplo, 0.79 se presenta como 79 %.
- Identificar Solola y la cobertura reportada. Resaltar el mes elegido en el bloque coincidente sin ocultar la serie completa.
- No calcular un indice anual sumando porcentajes ni presentar una media simple como el indice anual institucional sin denominadores adecuados.
- No recalcular el indice usando automaticamente el inventario anual: no hay habitaciones ocupadas/disponibles por mes ni evidencia suficiente de compatibilidad de cobertura.
- Una seleccion de municipio o procedencia no modifica ni relabela esta serie como si fuera municipal o por nacionalidad.

### **3.5.3. Visitas y ocupacion en los meses comparables**

Pregunta: "¿Cómo cambiaron las visitas al municipio y la ocupación hotelera de Sololá?".

**Aclaracion visible acordada:** incorporar una nota breve junto al titulo del cruce, antes de los paneles:

> Solo se comparan septiembre-diciembre de 2025: son los meses con datos tanto de visitas como de ocupacion hotelera.

Un tooltip opcional puede ampliar que ocupacion cubre enero de 2023 a diciembre de 2025, mientras movilidad mensual cubre septiembre-diciembre de 2025 y marzo-agosto de 2026. La explicacion esencial debe permanecer visible sin hover. Esta restriccion corresponde al cruce; las vistas independientes conservan su propia cobertura.

- Dos paneles alineados en el eje temporal de cuatro meses: afluencia del municipio/procedencia elegidos y ocupacion reportada para Solola.
- Cada panel tiene su eje y unidad. No utilizar dos ejes verticales superpuestos ni elegir limites independientes para fabricar coincidencias.
- Mostrar cantidades y porcentajes con etiquetas directas, periodos y escalas territoriales claramente escritos.
- La afluencia proviene de movilidad mensual; no de la suma de presencias diarias. Incluye las categorias de permanencia del universo seleccionado.
- La lectura es descriptiva. Cuatro meses y escalas territoriales distintas no permiten afirmar causalidad ni que las visitas de un municipio explican la ocupacion departamental.
- No atribuir a estos datos una conversion entre visitantes y huespedes, una tasa de ocupacion municipal o el porcentaje de visitantes que se hospedo.
- El contexto de ocupacion en este panel es una vista del mismo indicador departamental de la seccion anterior, limitada a la ventana comun; no es una medida nueva.

### **3.5.4. Visitas por municipio**

Pregunta: "¿Qué municipios recibieron más visitas este mes?".

- Barras horizontales con los diez municipios, ordenadas de mayor a menor por visitantes mensuales del universo nacional o extranjero seleccionado.
- Eje desde cero, cantidades visibles y municipio seleccionado resaltado. Mantener los otros municipios como contexto.
- `Relativa` significa comparacion entre valores reportados por municipio, no participacion porcentual de un total unico del lago.
- No sumar barras ni agregar una fila de total del lago. Tampoco convertir la suma de municipios en denominador.
- Este ranking de volumen cumple el requisito de subdestinos. El modulo 4 incorporara estadia, perfiles y la lectura de puerta de entrada frente a permanencia.

## **3.6. Reglas comunes**

- Mantener separados datos departamentales y municipales, universos nacional/extranjero, inventario y flujo.
- Declarar que la oferta cubre hospedajes, hoteles y pensiones registrados, sin asumir inclusion de alojamiento digital.
- No presentar ausencia de ocupacion en 2026 como cero ni extender esa serie mediante una proyeccion no solicitada.
- Conservar los valores de origen, las repeticiones entre cortes y los extremos respaldados por los boletines.
- No asignar paises de procedencia no identificados a nacionales o extranjeros; informar ese limite cuando corresponda.
- Los titulos, unidades, fechas y alcances se leen sin hover. La lectura principal no depende de conocer formulas o terminos tecnicos.

## **3.7. Resultado de la propuesta**

El alcance cubre los cuatro contenidos del modulo 3 sin suponer una oferta municipal que no existe. Los filtros quedan vinculados a fuentes que realmente admiten ese desglose. La comparacion detallada de perfiles municipales se reserva para el modulo 4, sin omitir aqui el ranking de afluencia solicitado.
