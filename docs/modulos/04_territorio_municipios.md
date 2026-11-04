# **4. Modulo 4: Territorio y perfiles de los diez municipios**

**Estado:** alcance funcional y pregunta del mapa aprobados. Se reviso la redaccion para lectura de personas no tecnicas. No se han implementado las vistas ni obtenido los datos geograficos de apoyo.

**Lenguaje de la interfaz:** las preguntas de las tablas y de cada grafico son textos para el lector y usan lenguaje natural y ortografia completa. El titulo formula una pregunta concreta; municipio, fechas, unidad y base de comparacion se indican junto a la vista. Los terminos tecnicos necesarios se explican brevemente y las formulas se conservan en la documentacion metodologica. La redaccion sencilla no cambia la medida ni permite afirmar mas de lo que muestran los datos.

## **4.1. Proposito y relacion con el reto**

Caracterizar los diez municipios riberenos segun volumen de visitas, estadia y comportamiento mensual. La pregunta principal es que perfiles de visita presentan y como cambian durante la cobertura disponible.

La guia principal asigna al Grupo 3 la caracterizacion territorial y el cuadrante analitico de los diez municipios, con una lectura de puertas de entrada frente a larga estancia. La [Guia de uso](../../data/raw/Guia_de_uso_de_los_datos_UVG.pdf), seccion 9, paginas 7-8, propone mapa, peso y evolucion mensual de los pueblos, volumen, estadia y participacion extranjera.

La participacion extranjera sobre un total combinado se sustituye por vistas separadas de nacionales y extranjeros, conforme a la aclaracion del catedratico comunicada por Bryan. El peso municipal se expresa mediante las cantidades reportadas, no como cuota de visitantes unicos del lago.

## **4.2. Preguntas y vistas propuestas**

| Pregunta | Representacion | Aporte al reto |
|---|---|---|
| ¿Qué municipios registran más visitas y cómo cambia esto de un mes a otro? | Mapa referencial con marcadores de volumen mensual | Comparar las visitas en el mapa |
| ¿Qué municipios reciben más visitas y en cuáles se quedan más tiempo? | Dispersion dividida en cuatro zonas, con volumen y estadia como ejes | Cuadrante analitico especializado |
| ¿En qué meses recibió más o menos visitas cada municipio? | Matriz de municipios por mes, con escala de color y valores | Evolucion comparable sin memorizar cuadros de una animacion |

No se repite el Top 10 de paises del modulo 1 ni se crea otro ranking aislado identico al del modulo 3. La lectura territorial utiliza las mismas definiciones de visitas y estadia para profundizar en sus relaciones.

## **4.3. Datos y cobertura**

Fuente principal: `data/processed/movilidad_mensual/movilidad_mensual_atitlan.csv`. Variables: `destino`, `fecha`, `pais`, `visitantes`, `dias_persona` y `es_consecutivo`.

Se dispone de diez meses observados por municipio y procedencia: septiembre-diciembre de 2025 y marzo-agosto de 2026. La comprobacion encontro una base positiva del segmento mayor a un dia en las 200 combinaciones de diez municipios, diez meses y dos procedencias; por tanto, se puede calcular su estadia ponderada en esta version.

No hay coordenadas ni archivos geograficos en esas tablas. Para construir el mapa se deberan incorporar ubicaciones municipales verificadas y documentar su fuente y condiciones de uso. La silueta decorativa del lago utilizada en la marca no sustituye esa informacion.

El mapa representara localizaciones de referencia. No se asumira que un limite municipal o un punto reproduce los poligonos de deteccion telefonica. Tampoco hay pares origen-destino para dibujar recorridos entre pueblos.

## **4.4. Filtros y seleccion**

| Control | Alcance | Comportamiento |
|---|---|---|
| Mes y anio | Mapa y cuadrante; columna resaltada de la matriz | Cambia los valores mensuales conservando el contexto historico de la matriz |
| Nacionales / extranjeros | Las tres vistas | Mantiene separados los universos, recalculando las medidas correspondientes |
| Municipio seleccionado en mapa o cuadrante | Resaltado vinculado | Resalta el mismo municipio en las otras vistas, sin ocultar los nueve restantes |

La seleccion de municipio es un detalle de exploracion, no un filtro que convierta el cuadrante en un punto unico. Debe poder restablecerse y funcionar tambien con controles accesibles, sin depender de un puntero.

La matriz conserva todos los meses; seleccionar uno no elimina las otras columnas. No se agregan filtros por pais, categoria de permanencia, tipo de hotel o perfil en esta primera version. La estadia se calcula siempre con la regla de pernocta, sin necesitar que el lector aplique ese filtro.

## **4.5. Definicion de las visualizaciones**

### **4.5.1. Visitas por municipio en el mapa**

Pregunta: "¿Qué municipios registran más visitas y cómo cambia esto de un mes a otro?".

La ubicacion de los municipios ayuda a interpretar sus cantidades de visitas. El mapa permite observar si los municipios con mas visitas estan cerca entre si o en distintas partes del lago, y si eso cambia con el mes o la procedencia. No se da por hecho que exista concentracion ni se suman municipios para fabricar personas unicas del lago.

- Ubicar los diez municipios mediante puntos verificados sobre una base territorial legible.
- Codificar el volumen del mes y procedencia seleccionados mediante el area del marcador, con radio proporcional a la raiz cuadrada del valor. No utilizar diez colores para diez municipios.
- Incluir leyenda de tamanos, nombres legibles y cantidad del municipio seleccionado visible fuera del tooltip. El cuadrante ofrece la comparacion cuantitativa mas precisa mediante posicion sobre ejes.
- La seleccion de un marcador resalta ese municipio en cuadrante y matriz; no representa un desplazamiento.
- No colorear grandes areas como si hubieran sido medidas integramente ni rotular la superficie de un municipio como densidad de visitantes sin un denominador valido.
- No dibujar rutas, flechas de transferencias o flujos entre pueblos.
- El selector de mes actualiza los marcadores; no se necesita reproduccion automatica para cumplir la evolucion mensual.

### **4.5.2. Visitas y tiempo de estadia por municipio**

Pregunta: "¿Qué municipios reciben más visitas y en cuáles se quedan más tiempo?".

- Cada punto representa un municipio, con tamano uniforme.
- Eje horizontal: visitantes mensuales registrados, sumando las categorias de permanencia dentro del municipio y procedencia seleccionados.
- Eje vertical: estadia media ponderada solo de `mayor a 1 dia`, en dias por visitante: suma de dias-persona dividida entre suma de visitantes de ese segmento.
- No utilizar el promedio de `permanencia_prom`, ni el promedio general que incluye visitas de paso.
- Los cuatro perfiles se nombran con lenguaje directo: mas visitas/estancias breves, mas visitas/estancias largas, menos visitas/estancias breves y menos visitas/estancias largas.
- Propuesta de referencia: mediana del volumen de los diez municipios y mediana de sus estadias en el mes y procedencia seleccionados. Las lineas y sus valores deben ser visibles y explicar que son referencias relativas a los municipios observados, no metas institucionales.
- Si un punto coincide con una referencia, identificarlo como tal sin forzar una conclusion extrema.
- Conservar nombres o etiquetas que permitan reconocer los municipios. Resaltar el seleccionado y mantener legible el contexto de los demas.
- Revisar escalas que permitan leer la nube sin exagerar diferencias. Un eventual cambio de dominio debe ser explicito; no usar escala logaritmica sin justificarla y etiquetarla.

El perfil de muchas visitas y estadia breve es compatible con la interpretacion de puerta de entrada o visita de paso, pero no demuestra que las personas continuaron hacia otro municipio. La fuente no permite reconstruir itinerarios.

Las referencias se recalculan para el mes. Un cambio de cuadrante puede depender tanto de la medida del municipio como del cambio en la mediana de los otros; no se interpretara automaticamente como mejora o deterioro.

### **4.5.3. Visitas por municipio y mes**

Pregunta: "¿En qué meses recibió más o menos visitas cada municipio?".

- Filas: diez municipios; columnas: meses en orden cronologico con su anio, de septiembre de 2025 a agosto de 2026.
- Celda: visitantes mensuales del municipio y procedencia seleccionados. Color secuencial con leyenda de cantidades y escala comun para el conjunto de la vista, no una normalizacion independiente por fila sin declarar.
- Mostrar valores legibles, con formato compacto y unidad explicita cuando sea necesario. La lectura principal no debe depender de acertar el tono de color ni de abrir un tooltip.
- Enero-febrero de 2026 se muestran sin dato, con tratamiento distinto de cero. No se incluyen aqui estimaciones del modulo 2 como si fueran observaciones.
- Mantener un orden estable de filas para poder seguir cada municipio al cambiar el mes. No reordenar la matriz automaticamente por cada seleccion.
- Resaltar fila del municipio y columna del mes seleccionados. La seleccion de una celda puede coordinar ambos controles sin eliminar el resto del contexto.
- No agregar una fila de total del lago ni una columna de personas unicas del periodo.
- La vista describe los meses disponibles, mezclando dos anios; no es una comparacion interanual ni demuestra un patron estacional repetido.

## **4.6. Limites y claridad**

- Las tres vistas corresponden siempre a nacionales o extranjeros por separado. No se calcula cuota extranjera sobre un total combinado.
- No sumar municipios ni tratarlos como partes excluyentes del lago. Tampoco dividir por su suma para crear un peso poblacional.
- Los registros sin pais identificado no se asignan a una procedencia. Informar este limite cuando afecte la seleccion.
- No clasificar un municipio como mejor, peor, saturado o deficitario solo por su posicion. No existen aqui datos de gasto, satisfaccion o capacidad de carga para demostrarlo.
- La estadia no equivale a ocupacion hotelera municipal; las fuentes hoteleras son departamentales y se trabajan en el modulo 3.
- Distinguir meses sin cobertura, ceros y estadias no definidas. Si aparece denominador cero o dato ausente, mostrarlo y no forzar su inclusion en un cuadrante.
- Titulos, unidades, mes y procedencia visibles; etiquetas y anotaciones comprensibles para un lector no tecnico.

## **4.7. Resultado de la propuesta**

Mapa, cuadrante y matriz se complementan: distribucion espacial de la afluencia, perfil de volumen/estadia y evolucion mensual. Cubren el reto sin atribuir porcentajes comparables a universos distintos ni movimientos individuales inexistentes.

La propuesta requiere validar las ubicaciones cartograficas antes de implementar el mapa. La seleccion de la biblioteca, las escalas visuales definitivas y la distribucion de la interfaz se resolveran al construir, conservando las reglas analiticas aqui descritas.
