export type Origen = "Nacionales" | "Extranjeros";
export type Permanencia = "menor a 1 dia" | "mayor a 1 dia";

export type ResumenMensual = {
  municipio: string;
  mes: string;
  origen: Origen;
  visitas: string;
  diasPersona: string;
  visitasPaso: string;
  visitasPernocta: string;
  diasPernocta: string;
};

export type MercadoMensual = { municipio: string; mes: string; pais: string; visitas: string };
export type ProcedenciaDesconocida = { municipio: string; mes: string; registros: number; visitas: string };
export type DatosDemanda = {
  municipios: string[];
  mesesObservados: string[];
  resumenes: ResumenMensual[];
  mercados: MercadoMensual[];
  desconocidos: ProcedenciaDesconocida[];
};
