"use client";

import { CartesianGrid, Line, LineChart, ReferenceDot, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartLegend, ChartLegendContent, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import { formatearCompacto } from "../lib/formato";
import type { DatoGrafico, SerieGrafico } from "../types/graficos";

type GraficoLineasProps = {
  datos: DatoGrafico[];
  series: SerieGrafico[];
  descripcionAccesible: string;
  resaltado?: { etiqueta: string; valor: number };
};

export function GraficoLineas({ datos, series, descripcionAccesible, resaltado }: GraficoLineasProps) {
  const config: ChartConfig = Object.fromEntries(series.map((serie) => [serie.clave, { label: serie.nombre, color: serie.color }]));
  return (
    <ChartContainer config={config} className="h-80 w-full" aria-label={descripcionAccesible}>
      <LineChart accessibilityLayer data={datos} margin={{ top: 16, right: 16, bottom: 0, left: 0 }}>
        <CartesianGrid vertical={false} stroke="var(--border)" strokeDasharray="3 5" />
        <XAxis dataKey="etiqueta" tickLine={false} axisLine={false} tickMargin={12} minTickGap={20} />
        <YAxis tickLine={false} axisLine={false} width={48} tickMargin={8} tickFormatter={formatearCompacto} />
        <ChartTooltip content={<ChartTooltipContent />} cursor={{ stroke: "var(--border)", strokeDasharray: "4 4" }} />
        <ChartLegend content={<ChartLegendContent />} />
        {series.map((serie) => <Line key={serie.clave} type="linear" dataKey={serie.clave} stroke={`var(--color-${serie.clave})`} strokeWidth={2.5} strokeDasharray={serie.discontinua ? "5 5" : undefined} dot={false} activeDot={{ r: 4 }} connectNulls={false} isAnimationActive={false} />)}
        {resaltado && <ReferenceDot x={resaltado.etiqueta} y={resaltado.valor} r={6} fill="var(--chart-1)" stroke="var(--card)" strokeWidth={2} ifOverflow="extendDomain" />}
      </LineChart>
    </ChartContainer>
  );
}
