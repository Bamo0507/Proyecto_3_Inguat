"use client";

import { CartesianGrid, Line, LineChart, ReferenceDot, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartLegend, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import { formatearCompacto } from "../lib/formato";
import type { DatoGrafico, SerieGrafico } from "../types/graficos";

const trazoDiscontinuo = "5 5";

type GraficoLineasProps = {
  datos: DatoGrafico[];
  series: SerieGrafico[];
  descripcionAccesible: string;
  ejeHorizontal?: string;
  ejeVertical?: string;
  resaltado?: { etiqueta: string; valor: number };
};

export function GraficoLineas({ datos, series, descripcionAccesible, ejeHorizontal, ejeVertical, resaltado }: GraficoLineasProps) {
  const config: ChartConfig = Object.fromEntries(series.map((serie) => [serie.clave, { label: serie.nombre, color: serie.color }]));
  return (
    <>
      {ejeVertical && <p className="mb-1 text-xs font-medium text-muted-foreground">{ejeVertical}</p>}
      <ChartContainer config={config} className="h-80 w-full" aria-label={descripcionAccesible}>
        <LineChart accessibilityLayer data={datos} margin={{ top: 16, right: 16, bottom: 0, left: 0 }}>
          <CartesianGrid vertical={false} stroke="var(--border)" strokeDasharray="3 5" />
          <XAxis dataKey="etiqueta" tickLine={false} axisLine={false} tickMargin={ejeHorizontal ? 8 : 12} minTickGap={20}
            height={ejeHorizontal ? 44 : undefined}
            label={ejeHorizontal ? { value: ejeHorizontal, position: "insideBottom", fill: "var(--muted-foreground)" } : undefined} />
          <YAxis tickLine={false} axisLine={false} width={48} tickMargin={8} tickFormatter={formatearCompacto} />
          <ChartTooltip content={<ChartTooltipContent />} cursor={{ stroke: "var(--border)", strokeDasharray: "4 4" }} />
          <ChartLegend content={() => (
            <ul className="flex flex-wrap justify-center gap-x-4 gap-y-1.5 pt-3">
              {series.map(({ clave, nombre, color, discontinua }) => (
                <li key={clave} className="flex items-center gap-1.5">
                  <svg aria-hidden="true" width="24" height="10" viewBox="0 0 24 10">
                    <path d="M1 5h22" stroke={color} strokeWidth={2.5}
                      strokeDasharray={discontinua ? trazoDiscontinuo : undefined} />
                    {discontinua && <circle cx="12" cy="5" r="3" fill="var(--card)" stroke={color} strokeWidth={2} />}
                  </svg>
                  {nombre}
                </li>
              ))}
            </ul>
          )} />
          {series.map((serie) => (
            <Line key={serie.clave} type="linear" dataKey={serie.clave}
              stroke={`var(--color-${serie.clave})`} strokeWidth={2.5}
              strokeDasharray={serie.discontinua ? trazoDiscontinuo : undefined}
              dot={serie.discontinua ? { r: 3, fill: "var(--card)", strokeWidth: 2, strokeDasharray: "none" } : false}
              activeDot={{ r: 4 }} connectNulls={false} isAnimationActive={false} />
          ))}
          {resaltado && (
            <ReferenceDot x={resaltado.etiqueta} y={resaltado.valor} r={6}
              fill="var(--chart-1)" stroke="var(--card)" strokeWidth={2} ifOverflow="extendDomain" />
          )}
        </LineChart>
      </ChartContainer>
    </>
  );
}
