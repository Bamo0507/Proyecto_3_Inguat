import { ArrowDownRight, ArrowUpRight, Minus, type LucideIcon } from "lucide-react";
import { Card, CardAction, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { formatearNumero, formatearPorcentaje } from "../lib/formato";

type IndicadorProps = {
  etiqueta: string;
  icono?: LucideIcon;
  valor: number | null;
  unidad?: string;
  periodo?: string;
  descripcion?: string;
  formato?: "numero" | "porcentaje";
  decimales?: number;
  comparacion?: { variacion: number; etiqueta: string };
  cargando?: boolean;
  textoSinDatos?: string;
  mensajeSinDatos?: string;
};

export function Indicador({ etiqueta, icono: IconoIndicador, valor, unidad, periodo, descripcion, formato = "numero", decimales = 0, comparacion, cargando = false, textoSinDatos = "Sin datos", mensajeSinDatos = "Sin información disponible para este período" }: IndicadorProps) {
  const disponible = valor !== null && Number.isFinite(valor);
  const valorFormateado = disponible
    ? formato === "porcentaje" ? formatearPorcentaje(valor, decimales) : formatearNumero(valor, decimales)
    : textoSinDatos;
  const tieneComparacion = disponible && comparacion && Number.isFinite(comparacion.variacion);
  const Icono = comparacion && comparacion.variacion > 0 ? ArrowUpRight : comparacion && comparacion.variacion < 0 ? ArrowDownRight : Minus;

  return (
    <Card className="indicador h-full gap-3" aria-busy={cargando}>
      <CardHeader className="gap-1.5">
        <CardTitle><h2>{etiqueta}</h2></CardTitle>
        {IconoIndicador && <CardAction><span className="indicador-emblema"><IconoIndicador aria-hidden="true" strokeWidth={1.5} /></span></CardAction>}
        {periodo && <CardDescription>{periodo}</CardDescription>}
      </CardHeader>
      <CardContent className="flex flex-col gap-2">
        <dl className="flex min-w-0 flex-col gap-3">
          <dt className="sr-only">{etiqueta}</dt>
          <dd className="flex min-h-14 items-center justify-between gap-3">
            <span className="flex min-w-0 flex-wrap items-baseline gap-2">
            {cargando ? <><Skeleton className="h-10 w-36" /><span className="sr-only">Cargando indicador</span></> : <>
              <span className="indicador-valor leading-none font-medium tabular-nums">{valorFormateado}</span>
              {disponible && unidad && <span className="text-sm text-muted-foreground">{unidad}</span>}
            </>}
            </span>
          </dd>
        </dl>
          <div className="indicador-contexto min-h-7 text-xs leading-relaxed text-muted-foreground">
            {!cargando && tieneComparacion && <span className="indicador-comparacion inline-flex items-center gap-1 font-medium">
              <Icono aria-hidden="true" className="size-3.5" />
              {comparacion.variacion > 0 ? "+" : ""}{formatearPorcentaje(comparacion.variacion)}
            </span>}
            {cargando ? <Skeleton className="h-4 w-48 max-w-full" /> : !disponible ? mensajeSinDatos : tieneComparacion ? comparacion.etiqueta : descripcion}
          </div>
      </CardContent>
    </Card>
  );
}
