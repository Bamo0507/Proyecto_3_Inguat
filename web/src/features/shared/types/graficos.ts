export type DatoGrafico = {
  etiqueta: string;
  [clave: string]: string | number | null;
};

export type SerieGrafico = {
  clave: string;
  nombre: string;
  color: string;
  discontinua?: boolean;
};

export type EstadoVisual = "listo" | "cargando" | "vacio" | "error";
