import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { origenes, type DiaObservado, type MunicipioTemporal, type Origen } from "../types";

function leerCsv(texto: string) {
  const contenido = texto.replace(/^\uFEFF/, "").replace(/\r?\n$/, "") + "\n";
  const campo = /(?:"((?:[^"]|"")*)"|([^",\r\n]*))(,|\r?\n|$)/y;
  const filas: string[][] = [];
  let fila: string[] = [];
  while (campo.lastIndex < contenido.length) {
    const resultado = campo.exec(contenido);
    if (!resultado) throw new Error("CSV de dinámica temporal inválido");
    fila.push(resultado[1]?.replaceAll('""', '"') ?? resultado[2]);
    if (resultado[3] !== ",") {
      filas.push(fila);
      fila = [];
    }
  }
  const [cabecera, ...registros] = filas;
  if (!cabecera || registros.some((registro) => registro.length !== cabecera.length)) {
    throw new Error("Estructura de CSV inválida");
  }
  return registros.map((registro) => Object.fromEntries(cabecera.map((nombre, i) => [nombre, registro[i]])));
}

function cantidad(valor: string) {
  const numero = Number(valor);
  if (!valor?.trim() || !Number.isFinite(numero) || numero < 0) throw new Error("Cantidad inválida");
  return numero;
}

function fechaIso(valor: string) {
  const fecha = valor?.slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(fecha ?? "")) throw new Error("Fecha inválida");
  const dia = new Date(fecha + "T00:00:00Z");
  if (!Number.isFinite(dia.getTime()) || dia.toISOString().slice(0, 10) !== fecha) throw new Error("Fecha inválida");
  return fecha;
}

function leerOrigen(valor: string): Origen {
  if (valor === "Nacionales" || valor === "Extranjeros") return valor;
  throw new Error("Origen inválido");
}

export async function cargarDinamicaTemporal(): Promise<MunicipioTemporal[]> {
  const directorio = resolve(process.cwd(), "../data/processed");
  const [diaria, mensual, validacion] = await Promise.all([
    readFile(resolve(directorio, "movilidad_diaria/movilidad_diaria_atitlan.csv"), "utf8"),
    readFile(resolve(directorio, "dinamica_temporal/serie_municipal_mensual.csv"), "utf8"),
    readFile(resolve(directorio, "dinamica_temporal/validacion_municipal.csv"), "utf8"),
  ]).then((archivos) => archivos.map(leerCsv));

  const municipios = new Map<string, MunicipioTemporal>();
  for (const fila of mensual) {
    const clave = fila.municipio.toUpperCase();
    if (!municipios.has(clave)) {
      municipios.set(clave, {
        nombre: fila.municipio,
        series: {
          Nacionales: { dias: [], meses: [], validacion: null },
          Extranjeros: { dias: [], meses: [], validacion: null },
        },
      });
    }
    const serie = municipios.get(clave)!.series[leerOrigen(fila.origen)];
    if (fila.tipo_dato !== "Observado" && fila.tipo_dato !== "Estimado") throw new Error("Tipo de dato inválido");
    serie.meses.push({ fecha: fechaIso(fila.fecha), visitantes: cantidad(fila.visitantes), tipo: fila.tipo_dato });
  }

  for (const fila of validacion) {
    const municipio = municipios.get(fila.municipio.toUpperCase());
    if (!municipio) throw new Error("Municipio de validación desconocido");
    const serie = municipio.series[leerOrigen(fila.origen)];
    if (serie.validacion) throw new Error("Validación duplicada");
    serie.validacion = {
      mae: cantidad(fila.mae),
      inicio: fechaIso(fila.inicio_validacion),
      fin: fechaIso(fila.fin_validacion),
      meses: cantidad(fila.meses_validacion),
    };
  }

  const agregados = new Map<string, DiaObservado>();
  for (const fila of diaria) {
    const municipio = municipios.get(fila.destino.trim().toUpperCase());
    if (!municipio) throw new Error("Municipio de movilidad diaria desconocido");
    const pais = fila.pais.trim().toUpperCase();
    if (!pais || pais === "\\N") continue;
    const origen = pais === "GUATEMALA" ? "Nacionales" : "Extranjeros";
    const fecha = fechaIso(fila.idfecha);
    const clave = [municipio.nombre, origen, fecha].join("|");
    const visitantes = cantidad(fila.cantidad_visitantes);
    const existente = agregados.get(clave);
    if (existente) {
      if (existente.evento !== fila.evento) throw new Error("Etiquetas de evento incompatibles para el mismo día");
      existente.visitantes += visitantes;
    } else {
      const dia = { fecha, visitantes, evento: fila.evento };
      agregados.set(clave, dia);
      municipio.series[origen].dias.push(dia);
    }
  }

  for (const municipio of municipios.values()) {
    for (const origen of origenes) {
      const serie = municipio.series[origen];
      serie.dias.sort((a, b) => a.fecha.localeCompare(b.fecha));
      serie.meses.sort((a, b) => a.fecha.localeCompare(b.fecha));
      if (!serie.validacion || serie.meses.length !== 12 || new Set(serie.meses.map((mes) => mes.fecha)).size !== 12) {
        throw new Error("Serie mensual incompleta");
      }
    }
  }
  if (!municipios.size || !agregados.size) throw new Error("Faltan las series municipales");
  return Array.from(municipios.values());
}
