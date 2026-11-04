"""Lectura fiel, validaciones y escritura auditable de tablas CSV."""
import warnings
from decimal import Decimal, InvalidOperation
import pandas as pd
from openpyxl import load_workbook
from config import FUENTES, RAW, PROCESSED, NULO_CSV, MARCADORES_NULO, COLUMNAS_INCIDENCIAS_CANTIDAD, ruta


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


def filas_origen(df, fuente, columnas_clave):
    """Recupera la fila CSV original por clave sin alterar las columnas finales."""
    original = leer(fuente, '01_ingesta')
    clave(original, columnas_clave, f'{fuente}: traza de origen')
    indices = original[columnas_clave].copy()
    indices['fila_csv'] = range(2, len(original) + 2)
    traza = df[columnas_clave].merge(indices, on=columnas_clave, how='left', validate='one_to_one', sort=False)
    exigir(traza['fila_csv'].notna().all(), 'No se pudo identificar la fila CSV original')
    return pd.Series(traza['fila_csv'].to_numpy(), index=df.index)


def registrar_cantidad(incidencias, fila, columna, original, motivo, clasificacion='rechazado_por_invalido'):
    incidencias.append({
        'fila_csv': int(fila), 'columna': columna,
        'valor_original': '' if pd.isna(original) else str(original),
        'valor_normalizado': NULO_CSV, 'motivo': motivo, 'clasificacion': clasificacion,
    })


def limpiar_cantidad(s, nombre, incidencias, origen, minimo=0, maximo=None, entera=False):
    """Conserva precision y filas; rechaza cantidades invalidas a nulo con evidencia."""
    texto = nulos(s)
    valores = []
    for indice, valor in texto.items():
        motivo = None
        clasificacion = 'rechazado_por_invalido'
        numero = None
        if pd.isna(valor):
            motivo = 'ausente_en_origen'
            clasificacion = 'ausente_en_origen'
        else:
            try:
                numero = Decimal(str(valor))
            except InvalidOperation:
                motivo = 'no_numerico'
            if numero is not None:
                if not numero.is_finite():
                    motivo = 'no_finito'
                elif minimo is not None and numero < Decimal(str(minimo)):
                    motivo = 'fuera_de_rango'
                elif maximo is not None and numero > Decimal(str(maximo)):
                    motivo = 'fuera_de_rango'
                elif entera and numero != numero.to_integral_value():
                    motivo = 'cantidad_fraccionaria'
                elif entera and numero > Decimal(2**63 - 1):
                    motivo = 'fuera_de_rango_entero'
        if motivo:
            valores.append(pd.NA)
            registrar_cantidad(incidencias, origen.loc[indice], nombre, s.loc[indice], motivo, clasificacion)
        else:
            valores.append(int(numero) if entera else str(valor))
    return pd.Series(valores, index=s.index, dtype='Int64' if entera else 'string')


def guardar_incidencias_cantidad(nombre, registros):
    """Escribe incluso un informe vacio, sin arrastrar incidencias de otra ejecucion."""
    evidencia = pd.DataFrame(registros, columns=COLUMNAS_INCIDENCIAS_CANTIDAD)
    guardar(evidencia, nombre, 'incidencias_tipado')
