import { cociente, comparar, numero, sumar } from "./decimal";
import type { DatosDemanda, MercadoMensual, Origen, ResumenMensual } from "./tipos";

export type ResumenSeleccion = {
  promedioMensual: number | null;
  mesesConDato: number;
  diasPersona: number | null;
  estadia: number | null;
  visitasMes: number | null;
  serie: { mes: string; visitas: number | null }[];
  ranking: MercadoMensual[];
  composicion: { origen: Origen; paso: number | null; pernocta: number | null; total: string }[];
  procedenciaDesconocida: { registros: number; visitas: string };
};

export function calendario(inicio: string, fin: string): string[] {
  const [anioInicial, mesInicial] = inicio.split("-").map(Number);
  const [anioFinal, mesFinal] = fin.split("-").map(Number);
  const salida: string[] = [];
  for (let anio = anioInicial, mes = mesInicial; anio < anioFinal || (anio === anioFinal && mes <= mesFinal);) {
    salida.push(`${anio}-${String(mes).padStart(2, "0")}`);
    mes++;
    if (mes === 13) { anio++; mes = 1; }
  }
  return salida;
}

export function etiquetaMes(mes: string): string {
  const nombres = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];
  const [anio, numeroMes] = mes.split("-").map(Number);
  return `${nombres[numeroMes - 1]} de ${anio}`;
}

export function etiquetaEjeMes(mes: string): string {
  const cortos = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
  const [anio, numeroMes] = mes.split("-").map(Number);
  return `${cortos[numeroMes - 1]} ${String(anio).slice(2)}`;
}

function encontrar(datos: DatosDemanda, municipio: string, mes: string, origen: Origen): ResumenMensual | undefined {
  return datos.resumenes.find((r) => r.municipio === municipio && r.mes === mes && r.origen === origen);
}

export function calcularSeleccion(datos: DatosDemanda, municipio: string, mes: string, origen: Origen): ResumenSeleccion {
  const meses = datos.resumenes.filter((r) => r.municipio === municipio && r.origen === origen);
  const totalPeriodo = meses.reduce((acumulado, r) => sumar(acumulado, r.visitas), "0");
  const actual = encontrar(datos, municipio, mes, origen);
  const ranking = datos.mercados.filter((r) => r.municipio === municipio && r.mes === mes)
    .sort((a, b) => comparar(b.visitas, a.visitas) || a.pais.localeCompare(b.pais, "es"))
    .slice(0, 10);
  const composicion: ResumenSeleccion["composicion"] = (["Nacionales", "Extranjeros"] as const).map((grupo) => {
    const r = encontrar(datos, municipio, mes, grupo);
    if (!r || comparar(r.visitas, "0") === 0) return { origen: grupo, paso: null, pernocta: null, total: r?.visitas ?? "0" };
    return { origen: grupo, paso: cociente(r.visitasPaso, r.visitas), pernocta: cociente(r.visitasPernocta, r.visitas), total: r.visitas };
  });
  const desconocida = datos.desconocidos.find((r) => r.municipio === municipio && r.mes === mes);
  return {
    promedioMensual: meses.length ? cociente(totalPeriodo, String(meses.length)) : null,
    mesesConDato: meses.length,
    diasPersona: actual ? numero(actual.diasPersona) : null,
    estadia: actual ? cociente(actual.diasPernocta, actual.visitasPernocta) : null,
    visitasMes: actual ? numero(actual.visitas) : null,
    serie: calendario(datos.mesesObservados[0], datos.mesesObservados.at(-1) ?? datos.mesesObservados[0]).map((m) => ({ mes: m, visitas: (() => { const r = encontrar(datos, municipio, m, origen); return r ? numero(r.visitas) : null; })() })),
    ranking,
    composicion,
    procedenciaDesconocida: { registros: desconocida?.registros ?? 0, visitas: desconocida?.visitas ?? "0" },
  };
}
