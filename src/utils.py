"""Lectura fiel, validaciones y escritura auditable de tablas CSV."""
import warnings
from decimal import Decimal, InvalidOperation
import pandas as pd
from openpyxl import load_workbook
from config import FUENTES, RAW, PROCESSED, NULO_CSV, MARCADORES_NULO


def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)


def esquema(df, columnas):
    exigir(list(df.columns)==columnas, f'Esquema distinto: {list(df.columns)}; esperado {columnas}')


def filas(df, n, contexto):
    exigir(len(df)==n, f'{contexto}: {len(df)} filas; esperado {n}')


def clave(df, columnas, contexto):
    repetidas = df.duplicated(columnas, keep=False)
    exigir(not repetidas.any(), f'{contexto}: {int(repetidas.sum())} filas con clave repetida {columnas}')


def leer_excel(nombre):
    cfg=FUENTES[nombre]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        libro=load_workbook(RAW/cfg['archivo'], read_only=True, data_only=True)
    try:
        hoja=libro[cfg['hoja']]
        hoja.reset_dimensions()  # El XML declara A1:A1 aunque contiene miles de filas.
        iterador=hoja.iter_rows(values_only=True)
        cabecera=[str(x) if x is not None else '' for x in next(iterador)]
        exigir(cabecera==cfg['columnas'], f'{nombre}: cabecera inesperada {cabecera}')
        registros=[]
        for fila in iterador:
            exigir(len(fila)==len(cabecera), f'{nombre}: ancho de fila distinto')
            registros.append(['' if x is None else str(x) for x in fila])
        return pd.DataFrame(registros, columns=cabecera, dtype='string')
    finally:
        libro.close()


def leer_raw(nombre):
    cfg=FUENTES[nombre]
    if 'hoja' in cfg:
        return leer_excel(nombre)
    df=pd.read_csv(RAW/cfg['archivo'], dtype='string', keep_default_na=False, na_filter=False)
    esquema(df,cfg['columnas'])
    return df


def ruta(nombre, etapa):
    return PROCESSED/nombre/f'{etapa}.csv'


def guardar(df,nombre,etapa):
    destino=ruta(nombre,etapa)
    destino.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(destino,index=False,na_rep=NULO_CSV,lineterminator='\n')
    print(f'{nombre}/{etapa}: {len(df)} filas -> {destino.relative_to(PROCESSED.parent.parent)}')


def leer(nombre,etapa):
    return pd.read_csv(ruta(nombre,etapa), dtype='string', keep_default_na=False, na_values=[NULO_CSV], low_memory=False)


def nulos(s):
    return s.astype('string').map(lambda x: pd.NA if pd.isna(x) or str(x).strip().casefold() in MARCADORES_NULO else x)


def entero(s, nombre, minimo=None, maximo=None):
    texto=nulos(s)
    numero=pd.to_numeric(texto,errors='coerce')
    invalido=texto.notna() & (numero.isna() | (numero%1!=0))
    exigir(not invalido.any(),f'{nombre}: {int(invalido.sum())} enteros invalidos')
    if minimo is not None: exigir((numero.dropna()>=minimo).all(),f'{nombre}: valor menor que {minimo}')
    if maximo is not None: exigir((numero.dropna()<=maximo).all(),f'{nombre}: valor mayor que {maximo}')
    return numero.astype('Int64')


def decimal(s,nombre,minimo=None,maximo=None,permitir_nulos=False):
    texto=nulos(s)
    valores=[]
    for valor in texto:
        if pd.isna(valor):
            exigir(permitir_nulos,f'{nombre}: cantidad ausente')
            valores.append(pd.NA)
            continue
        try:
            numero=Decimal(str(valor))
        except InvalidOperation as exc:
            raise ValueError(f'{nombre}: numero invalido {valor!r}') from exc
        exigir(numero.is_finite(),f'{nombre}: numero no finito')
        if minimo is not None: exigir(numero>=Decimal(str(minimo)),f'{nombre}: valor menor que {minimo}')
        if maximo is not None: exigir(numero<=Decimal(str(maximo)),f'{nombre}: valor mayor que {maximo}')
        valores.append(str(valor))
    return pd.Series(valores,index=s.index,dtype='string')


def fecha(s,nombre):
    d=pd.to_datetime(s, errors='coerce', format='mixed')
    exigir(d.notna().all(),f'{nombre}: fecha invalida')
    return d


def incidencia(nombre,df):
    guardar(df,nombre,'incidencias')
