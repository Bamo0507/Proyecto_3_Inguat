"""Transformaciones por fuente; cada función corresponde a una etapa numerada."""
import json
import unicodedata
from decimal import Decimal
import pandas as pd
from openpyxl import load_workbook
from config import FUENTES, MUNICIPIOS, MESES, VIAS, TIPOS_ALOJAMIENTO, RAW, SALIDAS_FINALES, COLUMNAS_SALIDA, FORMATO_FECHA, FORMATO_FECHA_HORA
from utils import leer_raw, leer, guardar, exigir, esquema, filas, clave, nulos, entero, decimal, fecha, incidencia


def ingesta(nombre):
    df=leer_raw(nombre)
    esquema(df,FUENTES[nombre]['columnas'])
    esperado=FUENTES[nombre]['filas'] if nombre.startswith('movilidad') or nombre=='migracion' else (792 if nombre=='ocupacion_hotelera' else 330)
    filas(df,esperado,f'{nombre}: ingesta')
    guardar(df,nombre,'01_ingesta')
    if nombre=='migracion':
        libro=load_workbook(RAW/FUENTES[nombre]['archivo'],read_only=True,data_only=True)
        try:
            hoja=libro['Notas']
            hoja.reset_dimensions()
            notas=[]
            for numero, valores in enumerate(hoja.iter_rows(values_only=True),start=1):
                notas.append({'fila_excel':numero,'tema':'' if len(valores)<1 or valores[0] is None else str(valores[0]),'descripcion':'' if len(valores)<2 or valores[1] is None else str(valores[1])})
            exigir(len(notas)==10,'Hoja Notas: filas inesperadas')
            guardar(pd.DataFrame(notas),nombre,'01_notas')
        finally:
            libro.close()


def seleccion(nombre):
    df=leer(nombre,'01_ingesta')
    esquema(df,FUENTES[nombre]['columnas'])
    if nombre.startswith('movilidad'):
        esperados=MUNICIPIOS if nombre=='movilidad_mensual' else {m.upper() for m in MUNICIPIOS}
        exigir(set(df['destino'])==esperados, f'{nombre}: municipios inesperados')
        exigir(df['sub_grupo'].nunique()==1,f'{nombre}: sub_grupo no constante')
        df=df.drop(columns=['sub_grupo'])
    elif nombre=='migracion':
        clave(df,['Año','Mes cod','Vía','Frontera','País','Tipo de Viajero','Agrupación Residencia'],'migracion original')
        codigo=df['Frontera'].str.extract(r'^(\d{2})\s',expand=False)
        esperada=codigo.map(VIAS).where(codigo.notna(),df['Frontera'].map({'Cruceros':'Marítima'}))
        exigir(esperada.notna().all() and int(df['Vía'].ne(esperada).sum())==93,'Catalogo de vias de la fuente no concilia')
        exigir(set(df['Tipo de Viajero'].dropna())=={'Turista','Excursionista','Viajero','Cruceristas'},'Tipos de viajero inesperados')
        tipos=df['Tipo de Viajero'].isin(['Turista','Excursionista'])
        exigir(int(tipos.sum())==137642,'Filtro de tipos no concilia')
        df=df.loc[tipos & df['País'].ne('Guatemala')].copy()
        filas(df,132894,'migracion: poblacion objetivo')
    else:
        df=df.loc[df['departamento'].eq('Sololá')].copy()
        filas(df,FUENTES[nombre]['filas'],f'{nombre}: Solola')
        exigir(df['departamento'].eq('Sololá').all(),'Filtro de departamento fallido')
        if nombre=='ocupacion_hotelera': clave(df,['anio','mes','departamento'],nombre)
        else: clave(df,['anio','trimestre','departamento','tipo_alojamiento'],nombre)
    guardar(df,nombre,'02_seleccion')


def normalizacion(nombre):
    df=leer(nombre,'02_seleccion')
    if nombre.startswith('movilidad'):
        df['pais']=nulos(df['pais'])
        if nombre=='movilidad_mensual':
            exigir(int(df['pais'].isna().sum())==25,'Pais mensual: faltantes inesperados')
        else:
            reparables=df['pais'].eq('ESPAÃ±A').fillna(False)
            exigir(int(reparables.sum())==1376,'Espana: recuento inesperado')
            df.loc[reparables,'pais']='ESPAÑA'
            exigir(int(df['pais'].isna().sum())==41,'Pais diario: faltantes inesperados')
        guardar(df,nombre,'03_normalizacion')
        return
    # Migración: incidencias trazables sobre todas las filas originales.
    # Recupera la fila de origen mediante la clave original, sin deduplicar.
    fuente=leer(nombre,'01_ingesta')
    identificador=fuente.reset_index().rename(columns={'index':'indice_origen'})
    identificador['indice_origen']=identificador['indice_origen']+2
    claves=list(FUENTES[nombre]['columnas'])
    df=df.merge(identificador[claves+['indice_origen']],on=claves,how='left',validate='one_to_one',sort=False)
    exigir(df['indice_origen'].notna().all(),'Fila de origen sin traza')
    incidencias=[]
    def agregar(mask,col,anterior,nuevo,motivo):
        for i in df.index[mask.fillna(False)]:
            incidencias.append({'fila_excel':int(df.at[i,'indice_origen']),'columna':col,'valor_original':str(anterior.loc[i]),'valor_normalizado':str(nuevo.loc[i]),'motivo':motivo})
    codigo=df['Frontera'].str.extract(r'^(\d{2})\s',expand=False)
    via_esperada=codigo.map(VIAS)
    via_esperada=via_esperada.where(codigo.notna(),df['Frontera'].map({'Cruceros':'Marítima'}))
    exigir(via_esperada.notna().all(),'Frontera sin via en catalogo')
    reparacion=df['Vía'].ne(via_esperada)
    exigir(int(reparacion.sum())==92,'Vias discrepantes en la poblacion seleccionada')
    agregar(reparacion,'via',df['Vía'],via_esperada,'catalogo_frontera')
    df['Vía']=via_esperada
    normal=df['País'].map(lambda x: unicodedata.normalize('NFC',str(x)).strip().casefold())
    normal_fuente=fuente['País'].map(lambda x: unicodedata.normalize('NFC',str(x)).strip().casefold())
    canon=fuente.groupby(normal_fuente,sort=False)['País'].first()
    pais_nuevo=normal.map(canon)
    pais_cambio=df['País'].ne(pais_nuevo)
    agregar(pais_cambio,'pais',df['País'],pais_nuevo,'variante_mayusculas')
    mapa_paises=pd.DataFrame({'pais_original':df.loc[pais_cambio,'País'],'pais_normalizado':pais_nuevo.loc[pais_cambio]}).drop_duplicates().sort_values('pais_original')
    guardar(mapa_paises,nombre,'mapa_paises')
    df['País']=pais_nuevo
    residencia_nueva=df['Agrupación Residencia'].replace({'Resto de mundo':'Resto del Mundo'})
    agregar(df['Agrupación Residencia'].ne(residencia_nueva),'agrupacion_residencia',df['Agrupación Residencia'],residencia_nueva,'variante_escritura')
    df['Agrupación Residencia']=residencia_nueva
    for col,valor in [('Región dos','0'),('Regiones OMT','0x2a')]:
        mask=df[col].eq(valor)
        nuevo=df[col].mask(mask)
        agregar(mask,{'Región dos':'region_dos','Regiones OMT':'regiones_omt'}[col],df[col],nuevo,'clasificacion_invalida')
        df[col]=nuevo
    for col in ['País','Región','Región dos','Regiones OMT','MCEO','Agrupación Residencia']:
        df[col]=nulos(df[col])
    llave=['Año','Mes cod','Vía','Frontera','País','Tipo de Viajero','Agrupación Residencia']
    colisiones=df.duplicated(llave,keep=False)
    exigir(int(colisiones.sum())==40,'Colisiones normalizadas distintas de las 40 documentadas')
    for i in df.index[colisiones]:
        anterior=fuente.iloc[int(df.at[i,'indice_origen'])-2]
        incidencias.append({'fila_excel':int(df.at[i,'indice_origen']),'columna':'clave_completa','valor_original':json.dumps({c:str(anterior[c]) for c in llave},ensure_ascii=False),'valor_normalizado':json.dumps({c:str(df.at[i,c]) for c in llave},ensure_ascii=False),'motivo':'colision_conocida_conservada'})
    for col in ['Región dos','Regiones OMT']:
        esperado=13 if col=='Región dos' else 5
        exigir(int(df[col].isna().sum())==esperado,f'{col}: invalidos inesperados')
    evidencia=pd.DataFrame(incidencias).sort_values(['fila_excel','columna'])
    incidencia(nombre,evidencia)
    guardar(df,nombre,'03_normalizacion')


def tipado(nombre):
    etapa='03_normalizacion' if nombre in ['movilidad_mensual','movilidad_diaria','migracion'] else '02_seleccion'
    df=leer(nombre,etapa)
    if nombre=='movilidad_mensual':
        df=df.drop(columns=['permanencia_prom'])
        df['anio']=entero(df['anio'],'anio',2025,2026)
        df['mes']=entero(df['mes'],'mes',1,12)
        d=fecha(df['fecha'],'fecha')
        exigir((d.dt.year==df['anio']).all() and (d.dt.month==df['mes']).all(),'Fecha mensual incoherente')
        df['fecha']=d.dt.strftime(FORMATO_FECHA_HORA)
        for c in ['visitantes','dias_persona']: df[c]=decimal(df[c],c,0)
        clave(df,['destino','fecha','pais','es_consecutivo'],nombre)
        exigir(set(df['destino'])==MUNICIPIOS,'Municipios mensuales')
        exigir(set(df['es_consecutivo'])=={'mayor a 1 dia','menor a 1 dia'},'Permanencia inesperada')
        filas(df,9860,nombre)
        exigir(not ((df['anio']==2026)&df['mes'].isin([1,2])).any(),'Meses no observados agregados')
    elif nombre=='movilidad_diaria':
        df=df.rename(columns={'Week':'num_semana'})
        for c,lo,hi in [('anio',2025,2026),('mes',1,12),('num_semana',1,53)]: df[c]=entero(df[c],c,lo,hi)
        d=fecha(df['idfecha'],'idfecha')
        exigir((d.dt.year==df['anio']).all() and (d.dt.month==df['mes']).all(),'Fecha diaria incoherente')
        exigir((d.dt.isocalendar().week.astype('Int64')==df['num_semana']).all(),'Semana ISO incoherente')
        dias={0:'lunes',1:'martes',2:'miercoles',3:'jueves',4:'viernes',5:'sabado',6:'domingo'}
        normal=lambda x: ''.join(c for c in unicodedata.normalize('NFKD',str(x).casefold()) if not unicodedata.combining(c))
        exigir((df['dia_semana'].map(normal)==d.dt.dayofweek.map(dias)).all(),'Dia de semana incoherente')
        df['idfecha']=d.dt.strftime(FORMATO_FECHA_HORA)
        df['cantidad_visitantes']=decimal(df['cantidad_visitantes'],'cantidad_visitantes',0)
        clave(df,['destino','idfecha','pais'],nombre)
        filas(df,82952,nombre)
    elif nombre=='migracion':
        df=df.rename(columns={'Año':'anio','Mes cod':'mes','Vía':'via','Frontera':'frontera','País':'pais','Región':'region','Región dos':'region_dos','Regiones OMT':'regiones_omt','MCEO':'mceo','Agrupación Residencia':'agrupacion_residencia','Tipo de Viajero':'tipo_viajero','Viajero':'viajeros'})
        df['anio']=entero(df['anio'],'anio',2009,2026)
        df['mes']=entero(df['mes'],'mes',1,12)
        exigir((df['Mes']==df['mes'].map(MESES)).all(),'Nombre de mes incoherente')
        df['fecha']=pd.to_datetime(dict(year=df['anio'],month=df['mes'],day=1)).dt.strftime(FORMATO_FECHA)
        df['viajeros']=decimal(df['viajeros'],'viajeros',0)
        df=df.drop(columns=['Mes','indice_origen'])
        df=df[COLUMNAS_SALIDA[nombre]]
        exigir(set(df['tipo_viajero'])=={'Turista','Excursionista'} and not df['pais'].eq('Guatemala').any(),'Poblacion migracion')
        filas(df,132894,nombre)
    elif nombre=='ocupacion_hotelera':
        df['anio']=entero(df['anio'],'anio',2023,2025)
        df['mes']=entero(df['mes'],'mes',1,12)
        df['indice_ocupacion']=decimal(df['indice_ocupacion'],'indice_ocupacion',0,1,permitir_nulos=True)
        exigir(df['indice_ocupacion'].notna().all(),'Indice ausente: revisar incidencia')
        df['fecha']=pd.to_datetime(dict(year=df['anio'],month=df['mes'],day=1)).dt.strftime(FORMATO_FECHA)
        df=df[['fecha','indice_ocupacion']]
        clave(df,['fecha'],nombre)
        exigir(set(df['fecha'])==set(pd.date_range('2023-01-01','2025-12-01',freq='MS').strftime('%Y-%m-%d')),'Cobertura ocupacion')
        filas(df,36,nombre)
    else:
        df['anio']=entero(df['anio'],'anio',2022,2026)
        df['trimestre']=entero(df['trimestre'],'trimestre',1,4)
        for c in ['establecimientos','habitaciones','plazas_cama']:
            df[c]=entero(df[c],c,0)
            exigir(df[c].notna().all(),f'{c}: cantidad ausente')
        exigir(set(df['tipo_alojamiento'])==TIPOS_ALOJAMIENTO,'Tipos de alojamiento inesperados')
        exigir((df['habitaciones']>=df['establecimientos']).all() and (df['plazas_cama']>=df['habitaciones']).all(),'Capacidad incoherente')
        df=df.drop(columns=['departamento'])
        clave(df,['anio','trimestre','tipo_alojamiento'],nombre)
        exigir(set(zip(df['anio'],df['trimestre']))=={(2022,4),(2023,4),(2024,4),(2025,4),(2026,1)},'Cortes inesperados')
        filas(df,15,nombre)
    esquema(df,COLUMNAS_SALIDA[nombre])
    guardar(df,nombre,'04_tipado' if nombre in ['movilidad_mensual','movilidad_diaria','migracion'] else '03_tipado')
    guardar(df,nombre,SALIDAS_FINALES[nombre][0])


def mensual_migracion():
    nombre='migracion'
    df=leer(nombre,'04_tipado')
    df['viajeros']=decimal(df['viajeros'],'viajeros',0)
    df['viajeros_decimal']=df['viajeros'].map(Decimal)
    fechas=pd.date_range('2009-01-01','2026-06-01',freq='MS').strftime(FORMATO_FECHA)
    agregado=df.groupby('fecha').agg(viajeros=('viajeros_decimal','sum'),registros=('viajeros','size')).reindex(fechas)
    agregado.index.name='fecha'
    agregado.loc[agregado['registros'].isna(),'viajeros']=pd.NA
    agregado['registros']=agregado['registros'].fillna(0).astype('Int64')
    agregado=agregado.reset_index()
    agregado['conjunto']='historico'
    agregado.loc[agregado['fecha'].between('2023-01-01','2025-12-01'),'conjunto']='ajuste'
    agregado.loc[agregado['fecha'].between('2026-01-01','2026-06-01'),'conjunto']='evaluacion'
    exigir(len(agregado)==210 and int(agregado['viajeros'].isna().sum())==5,'Rejilla mensual migracion')
    exigir(agregado.loc[agregado['conjunto'].isin(['ajuste','evaluacion']),'viajeros'].gt(0).all(),'Ventana no positiva')
    exigir(int((agregado['conjunto']=='ajuste').sum())==36 and int((agregado['conjunto']=='evaluacion').sum())==6,'Ventanas migracion')
    exigir(sum((v for v in agregado['viajeros'] if pd.notna(v)),Decimal(0))==sum(df['viajeros_decimal'],Decimal(0)),'Suma migracion no concilia')
    agregado['viajeros']=agregado['viajeros'].map(lambda v: str(v) if pd.notna(v) else pd.NA)
    guardar(agregado,nombre,'05_mensual')
    guardar(agregado,nombre,SALIDAS_FINALES[nombre][1])
    guardar(agregado.loc[agregado['conjunto']=='ajuste'],nombre,SALIDAS_FINALES[nombre][2])
    guardar(agregado.loc[agregado['conjunto']=='evaluacion'],nombre,SALIDAS_FINALES[nombre][3])
