import { readFile } from "node:fs/promises";
import path from "node:path";
import { comparar, sumar } from "./decimal";
import type { DatosDemanda, MercadoMensual, Origen, Permanencia, ProcedenciaDesconocida, ResumenMensual } from "./tipos";

const columnas = ["destino", "fecha", "pais", "es_consecutivo", "visitantes", "dias_persona"] as const;
const archivo = "data/processed/movilidad_mensual/movilidad_mensual_atitlan.csv";

/** Lector CSV con comillas dobles, comas y saltos de línea dentro de campos. */
export function leerCsv(texto: string): string[][] {
  const filas: string[][] = [];
  let fila: string[] = [];
  let campo = "";
  let entreComillas = false;
  let despuesDeComillas = false;
  for (let i = 0; i < texto.length; i++) {
    const c = texto[i];
    if (entreComillas) {
      if (c === '"' && texto[i + 1] === '"') { campo += '"'; i++; }
      else if (c === '"') { entreComillas = false; despuesDeComillas = true; }
      else campo += c;
      continue;
    }
    if (despuesDeComillas && c !== "," && c !== "\n" && c !== "\r") throw new Error("CSV: texto inesperado después de comillas");
    if (c === '"' && campo === "" && !despuesDeComillas) { entreComillas = true; continue; }
    if (c === ",") { fila.push(campo); campo = ""; despuesDeComillas = false; continue; }
    if (c === "\n" || c === "\r") {
      if (c === "\r" && texto[i + 1] === "\n") i++;
      fila.push(campo); filas.push(fila); fila = []; campo = ""; despuesDeComillas = false;
      continue;
    }
    if (c === '"') throw new Error("CSV: comillas fuera de un campo citado");
    campo += c;
  }
  if (entreComillas) throw new Error("CSV: campo citado sin cierre");
  if (campo !== "" || fila.length > 0 || despuesDeComillas) { fila.push(campo); filas.push(fila); }
  return filas;
}

export function prepararDatosDemanda(texto: string): DatosDemanda {
  const filas = leerCsv(texto);
  const cabecera = filas.shift();
  if (!cabecera || !columnas.every((nombre) => cabecera.includes(nombre))) throw new Error("Faltan columnas de movilidad mensual");
  const indice = Object.fromEntries(cabecera.map((nombre, posicion) => [nombre, posicion]));
  const resumenes = new Map<string, ResumenMensual>();
  const mercados = new Map<string, MercadoMensual>();
  const desconocidos = new Map<string, ProcedenciaDesconocida>();
  const municipios = new Set<string>();
  const meses = new Set<string>();

  for (const fila of filas) {
    if (fila.length !== cabecera.length) throw new Error("CSV: cantidad de columnas inconsistente");
    const valor = (nombre: typeof columnas[number]) => fila[indice[nombre]];
    const municipio = valor("destino");
    const mes = valor("fecha").slice(0, 7);
    const pais = valor("pais");
    const permanencia = valor("es_consecutivo") as Permanencia;
    const visitas = valor("visitantes");
    const diasPersona = valor("dias_persona");
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(mes) || !["menor a 1 dia", "mayor a 1 dia"].includes(permanencia)) throw new Error("Mes o permanencia inválidos en movilidad mensual");
    if (comparar(visitas, "0") < 0 || comparar(diasPersona, "0") < 0) throw new Error("Cantidad negativa en movilidad mensual");
    municipios.add(municipio); meses.add(mes);
    if (pais === "\\N") {
      const clave = JSON.stringify([municipio, mes]);
      const actual = desconocidos.get(clave) ?? { municipio, mes, registros: 0, visitas: "0" };
      actual.registros++;
      actual.visitas = sumar(actual.visitas, visitas);
      desconocidos.set(clave, actual);
      continue;
    }
    const origen: Origen = pais === "Guatemala" ? "Nacionales" : "Extranjeros";
    const clave = JSON.stringify([municipio, mes, origen]);
    const actual = resumenes.get(clave) ?? { municipio, mes, origen, visitas: "0", diasPersona: "0", visitasPaso: "0", visitasPernocta: "0", diasPernocta: "0" };
    actual.visitas = sumar(actual.visitas, visitas);
    actual.diasPersona = sumar(actual.diasPersona, diasPersona);
    if (permanencia === "menor a 1 dia") actual.visitasPaso = sumar(actual.visitasPaso, visitas);
    else {
      actual.visitasPernocta = sumar(actual.visitasPernocta, visitas);
      actual.diasPernocta = sumar(actual.diasPernocta, diasPersona);
    }
    resumenes.set(clave, actual);
    if (origen === "Extranjeros") {
      const clavePais = JSON.stringify([municipio, mes, pais]);
      const mercado = mercados.get(clavePais) ?? { municipio, mes, pais, visitas: "0" };
      mercado.visitas = sumar(mercado.visitas, visitas);
      mercados.set(clavePais, mercado);
    }
  }
  if (filas.length !== 9860 || municipios.size !== 10 || meses.size !== 10) throw new Error("Cobertura mensual distinta de la documentada");
  return {
    municipios: [...municipios].sort((a, b) => a.localeCompare(b, "es")),
    mesesObservados: [...meses].sort(),
    resumenes: [...resumenes.values()],
    mercados: [...mercados.values()],
    desconocidos: [...desconocidos.values()],
  };
}

export async function cargarDatosDemanda(): Promise<DatosDemanda> {
  const base = process.cwd();
  const raiz = path.basename(base) === "web" ? path.resolve(base, "..") : base;
  const contenido = await readFile(path.join(raiz, archivo), "utf8");
  return prepararDatosDemanda(contenido);
}
