import type { DiaObservado } from "../types";

const mesesLargos = new Intl.DateTimeFormat("es-GT", { month: "long", year: "numeric", timeZone: "UTC" });
const mesesCortos = new Intl.DateTimeFormat("es-GT", { month: "short", year: "2-digit", timeZone: "UTC" });
const diasSemana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
const fechaUtc = (fecha: string) => new Date(fecha + "T00:00:00Z");

export function nombreMes(mes: string, corto = false) {
  const texto = (corto ? mesesCortos : mesesLargos).format(fechaUtc(mes.slice(0, 7) + "-01"));
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}

export function calendarioDiario(dias: DiaObservado[], mes: string) {
  const [anio, numeroMes] = mes.split("-").map(Number);
  const disponibles = new Map(dias.map((dia) => [dia.fecha, dia]));
  return Array.from({ length: new Date(Date.UTC(anio, numeroMes, 0)).getUTCDate() }, (_, i) => {
    const fecha = mes + "-" + String(i + 1).padStart(2, "0");
    const observado = disponibles.get(fecha);
    return { fecha, visitantes: observado?.visitantes ?? null, evento: observado?.evento ?? null };
  });
}

function promedio(dias: DiaObservado[]) {
  return dias.length ? dias.reduce((suma, dia) => suma + dia.visitantes, 0) / dias.length : null;
}

export function resumirDias(dias: DiaObservado[], evento: string) {
  const regulares = dias.filter((dia) => dia.evento === "Regular");
  const seleccionados = evento ? dias.filter((dia) => dia.evento === evento) : [];
  const promedioRegular = promedio(regulares);
  const promedioEvento = promedio(seleccionados);
  return {
    promedioRegular,
    promedioEvento,
    diasRegulares: regulares.length,
    diasEvento: seleccionados.length,
    variacion: promedioRegular !== null && promedioRegular > 0 && promedioEvento !== null
      ? promedioEvento / promedioRegular - 1
      : null,
    semana: diasSemana.map((etiqueta, indice) => {
      const muestra = regulares.filter((dia) => (fechaUtc(dia.fecha).getUTCDay() + 6) % 7 === indice);
      return { etiqueta, promedio: promedio(muestra), dias: muestra.length, finDeSemana: indice >= 5 };
    }),
  };
}

export function nombreMunicipio(nombre: string) {
  return nombre.replace("Atitlan", "Atitlán").replace("Palopo", "Palopó").replace("Toliman", "Tolimán");
}
