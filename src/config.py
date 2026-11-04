"""Contratos y rutas del preprocesamiento del observatorio."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / 'data' / 'raw'
PROCESSED = RAIZ / 'data' / 'processed'
NULO_CSV = r'\N'
FORMATO_FECHA = '%Y-%m-%d'
FORMATO_FECHA_HORA = '%Y-%m-%d %H:%M:%S'
MARCADORES_NULO = {'', 'null', 'none', 'nan', 'na', 'n/a', 's/d'}

SALIDAS_FINALES = {
 'movilidad_mensual': ['movilidad_mensual_atitlan'],
 'movilidad_diaria': ['movilidad_diaria_atitlan'],
 'migracion': ['migracion_detalle','migracion_mensual','migracion_ajuste_2023_2025','migracion_evaluacion_2026_01_06'],
 'ocupacion_hotelera': ['ocupacion_solola'],
 'oferta_alojamiento': ['oferta_solola'],
}
COLUMNAS_SALIDA = {
 'movilidad_mensual': ['destino','anio','mes','pais','es_consecutivo','fecha','visitantes','dias_persona'],
 'movilidad_diaria': ['destino','anio','mes','idfecha','dia_semana','pais','num_semana','evento','cantidad_visitantes'],
 'migracion': ['anio','mes','via','frontera','pais','region','region_dos','regiones_omt','mceo','agrupacion_residencia','tipo_viajero','viajeros','fecha'],
 'ocupacion_hotelera': ['fecha','indice_ocupacion'],
 'oferta_alojamiento': ['anio','trimestre','tipo_alojamiento','establecimientos','habitaciones','plazas_cama'],
}

FUENTES = {
 'movilidad_mensual': {'archivo':'BD_moviidad_mensual.xlsx','hoja':'Atitlan','columnas':['destino','sub_grupo','anio','mes','pais','es_consecutivo','fecha','visitantes','dias_persona','permanencia_prom'],'filas':9860,'etapas':['01_ingesta','02_seleccion','03_normalizacion','04_tipado']},
 'movilidad_diaria': {'archivo':'BD_moviidad_diario.xlsx','hoja':'Atitlan','columnas':['destino','sub_grupo','anio','mes','idfecha','dia_semana','pais','Week','evento','cantidad_visitantes'],'filas':82952,'etapas':['01_ingesta','02_seleccion','03_normalizacion','04_tipado']},
 'migracion': {'archivo':'Base_Migracion_2009-2026jun.xlsx','hoja':'Datos','columnas':['Año','Mes cod','Mes','Vía','Frontera','País','Región','Región dos','Regiones OMT','MCEO','Agrupación Residencia','Tipo de Viajero','Viajero'],'filas':161036,'etapas':['01_ingesta','02_seleccion','03_normalizacion','04_tipado','05_mensual']},
 'ocupacion_hotelera': {'archivo':'indice_ocupacion_mensual_2023_2025_1.csv','columnas':['anio','mes','departamento','indice_ocupacion'],'filas':36,'etapas':['01_ingesta','02_seleccion','03_tipado']},
 'oferta_alojamiento': {'archivo':'oferta_hotelera_2022_2026.csv','columnas':['anio','trimestre','departamento','tipo_alojamiento','establecimientos','habitaciones','plazas_cama'],'filas':15,'etapas':['01_ingesta','02_seleccion','03_tipado']},
}
MUNICIPIOS = {'Panajachel','San Pedro La Laguna','Santiago Atitlan','San Juan La Laguna','San Marcos La Laguna','Santa Catarina Palopo','San Pablo La Laguna','San Antonio Palopo','San Lucas Toliman','Santa Cruz La Laguna'}
MESES = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
TIPOS_ALOJAMIENTO = {'Hospedaje','Hotel','Pensión'}
VIAS = {**{'01':'Aérea','02':'Aérea'}, **{f'{i:02}':'Marítima' for i in range(3,7)}, **{f'{i:02}':'Terrestre' for i in range(7,23)}}

# Contratos intermedios: cada etapa valida lo que recibe y lo que entrega.
COLUMNAS_ETAPA = {}
for _nombre, _fuente in FUENTES.items():
    _columnas = list(_fuente['columnas'])
    _contratos = {'01_ingesta': _columnas}
    _seleccion = [c for c in _columnas if c != 'sub_grupo'] if _nombre.startswith('movilidad') else list(_columnas)
    _contratos['02_seleccion'] = _seleccion
    if _nombre in {'movilidad_mensual', 'movilidad_diaria', 'migracion'}:
        _contratos['03_normalizacion'] = _seleccion + (['indice_origen'] if _nombre == 'migracion' else [])
        _contratos['04_tipado'] = COLUMNAS_SALIDA[_nombre]
    else:
        _contratos['03_tipado'] = COLUMNAS_SALIDA[_nombre]
    if _nombre == 'migracion':
        _contratos['05_mensual'] = ['fecha', 'viajeros', 'registros', 'conjunto']
    COLUMNAS_ETAPA[_nombre] = _contratos
    _fuente['filas_raw'] = {'ocupacion_hotelera': 792, 'oferta_alojamiento': 330}.get(_nombre, _fuente['filas'])
del _nombre, _fuente, _columnas, _contratos, _seleccion

COLUMNAS_INCIDENCIAS_CANTIDAD = [
    'fila_csv', 'columna', 'valor_original', 'valor_normalizado', 'motivo', 'clasificacion'
]


def ruta(nombre, etapa):
    """Ruta unica de cada tabla procesada, incluidos informes de incidencias."""
    return PROCESSED / nombre / f'{etapa}.csv'
