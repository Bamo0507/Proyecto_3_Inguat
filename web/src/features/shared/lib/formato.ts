export function formatearNumero(valor: number, decimales = 0) {
  return new Intl.NumberFormat("es-GT", {
    minimumFractionDigits: decimales,
    maximumFractionDigits: decimales,
  }).format(valor);
}

export function formatearCompacto(valor: number) {
  return new Intl.NumberFormat("es-GT", {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(valor);
}

export function formatearPorcentaje(valor: number, decimales = 1) {
  return new Intl.NumberFormat("es-GT", {
    style: "percent",
    minimumFractionDigits: decimales,
    maximumFractionDigits: decimales,
  }).format(valor);
}
