export const origenes = ["Nacionales", "Extranjeros"] as const;
export type Origen = (typeof origenes)[number];

export type DiaObservado = { fecha: string; visitantes: number; evento: string };
export type MesMunicipal = {
  fecha: string;
  visitantes: number;
  tipo: "Observado" | "Estimado";
};
export type ValidacionMunicipal = {
  mae: number;
  inicio: string;
  fin: string;
  meses: number;
};
export type SerieMunicipal = {
  dias: DiaObservado[];
  meses: MesMunicipal[];
  validacion: ValidacionMunicipal | null;
};
export type MunicipioTemporal = {
  nombre: string;
  series: Record<Origen, SerieMunicipal>;
};
