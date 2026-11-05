"""Genera la serie municipal y sus errores de validación para Dinámica temporal."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from config import MUNICIPIOS, SALIDAS_FINALES
from utils import clave, exigir, fecha, guardar, leer

NOMBRE = "dinamica_temporal"
CALENDARIO = pd.date_range("2025-09-01", "2026-08-01", freq="MS")
MESES_ESTIMADOS = pd.DatetimeIndex(["2026-01-01", "2026-02-01"])
MESES_VALIDACION = pd.DatetimeIndex(["2026-05-01", "2026-06-01"])
ORIGENES = ["Extranjeros", "Nacionales"]
CLAVE_SERIE = ["fecha", "municipio", "origen"]
PREDICTORES = ["paso_temporal", "ingresos_migratorios_observados"]


def ajustar(datos):
    entradas = datos[PREDICTORES].astype(float)
    objetivo = datos["visitantes"].to_numpy(dtype=float)
    return make_pipeline(StandardScaler(), LinearRegression()).fit(entradas, objetivo)


def main():
    movilidad = leer("movilidad_mensual", SALIDAS_FINALES["movilidad_mensual"][0])
    movilidad["fecha"] = fecha(movilidad["fecha"], "Movilidad mensual")
    movilidad = movilidad.rename(columns={"destino": "municipio"})
    pais = movilidad["pais"].str.strip().str.casefold()
    movilidad = movilidad.loc[pais.notna() & pais.ne("")].copy()
    movilidad["origen"] = np.where(pais.loc[movilidad.index].eq("guatemala"), "Nacionales", "Extranjeros")
    movilidad["visitantes"] = movilidad["visitantes"].astype("Float64")
    cantidades = movilidad["visitantes"].to_numpy(dtype=float, na_value=np.nan)
    exigir(np.isfinite(cantidades).all() and (cantidades >= 0).all(), "Cantidades de movilidad inválidas")
    observados = movilidad.groupby(CLAVE_SERIE, as_index=False)["visitantes"].sum()
    meses_observados = CALENDARIO.difference(MESES_ESTIMADOS)
    esperadas = pd.MultiIndex.from_product([meses_observados, sorted(MUNICIPIOS), ORIGENES], names=CLAVE_SERIE)
    claves_observadas = pd.MultiIndex.from_frame(observados[CLAVE_SERIE])
    exigir(len(claves_observadas) == len(esperadas) and claves_observadas.difference(esperadas).empty,
           "Cobertura municipal observada distinta de la prevista")

    migracion = leer("migracion", "migracion_mensual")
    migracion["fecha"] = fecha(migracion["fecha"], "Migración mensual")
    clave(migracion, ["fecha"], "Migración mensual")
    referencia = migracion.set_index("fecha")["viajeros"].astype("Float64")
    entradas = pd.DataFrame({
        "paso_temporal": range(len(CALENDARIO)),
        "ingresos_migratorios_observados": referencia.reindex(CALENDARIO),
    }, index=CALENDARIO.rename("fecha"))
    meses_ajuste_final = meses_observados[meses_observados <= MESES_VALIDACION.max()]
    requeridos = entradas.loc[meses_ajuste_final.union(MESES_ESTIMADOS), PREDICTORES[1]].to_numpy(dtype=float, na_value=np.nan)
    exigir(np.isfinite(requeridos).all() and (requeridos > 0).all(), "Falta migración observada en el período requerido")

    estimaciones = []
    errores = []
    for (municipio, origen), grupo in observados.groupby(["municipio", "origen"]):
        datos = grupo.set_index("fecha").join(entradas).loc[meses_ajuste_final]
        entrenamiento = datos.drop(index=MESES_VALIDACION)
        validacion = datos.loc[MESES_VALIDACION]
        diferencias = validacion["visitantes"].to_numpy(dtype=float) - ajustar(entrenamiento).predict(
            validacion[PREDICTORES].astype(float)
        )
        errores.append({
            "municipio": municipio, "origen": origen,
            "inicio_validacion": MESES_VALIDACION.min(), "fin_validacion": MESES_VALIDACION.max(),
            "meses_ajuste": len(entrenamiento), "meses_validacion": len(validacion),
            "mae": float(np.abs(diferencias).mean()), "rmse": float(np.sqrt(np.square(diferencias).mean())),
        })
        predicciones = ajustar(datos).predict(entradas.loc[MESES_ESTIMADOS, PREDICTORES].astype(float))
        exigir(np.isfinite(predicciones).all() and (predicciones >= 0).all(), f"Estimación inválida para {municipio}, {origen}")
        for mes, valor in zip(MESES_ESTIMADOS, predicciones):
            estimaciones.append({"fecha": mes, "municipio": municipio, "origen": origen, "visitantes": valor})

    serie = pd.concat([
        observados.assign(tipo_dato="Observado"),
        pd.DataFrame(estimaciones).assign(tipo_dato="Estimado"),
    ], ignore_index=True).sort_values(["municipio", "origen", "fecha"])
    validacion = pd.DataFrame(errores)
    clave(serie, CLAVE_SERIE, "Serie municipal")
    clave(validacion, ["municipio", "origen"], "Validación municipal")
    exigir(np.isfinite(validacion[["mae", "rmse"]].to_numpy()).all(), "Errores de validación no finitos")
    guardar(serie, NOMBRE, "serie_municipal_mensual")
    guardar(validacion, NOMBRE, "validacion_municipal")


if __name__ == "__main__":
    main()
