"use client";

import { Bar, BarChart, CartesianGrid, LabelList, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import { formatearCompacto } from "../lib/formato";
import type { DatoGrafico, SerieGrafico } from "../types/graficos";

type GraficoBarrasProps = {
  datos: DatoGrafico[];
  serie: SerieGrafico;
  descripcionAccesible: string;
  altura?: number;
  anchoEtiquetas?: number;
  mostrarValores?: boolean;
};

export function GraficoBarras({ datos, serie, descripcionAccesible, altura = 320, anchoEtiquetas = 68, mostrarValores = false }: GraficoBarrasProps) {
  const config: ChartConfig = { [serie.clave]: { label: serie.nombre, color: serie.color } };
  return (
    <ChartContainer config={config} className="w-full" style={{ height: altura }} aria-label={descripcionAccesible}>
      <BarChart accessibilityLayer data={datos} layout="vertical" margin={{ top: 8, right: mostrarValores ? 82 : 16, bottom: 0, left: 0 }}>
        <CartesianGrid horizontal={false} stroke="var(--border)" strokeDasharray="3 5" />
        <YAxis dataKey="etiqueta" type="category" axisLine={false} tickLine={false} width={anchoEtiquetas} tickMargin={8} />
        <XAxis type="number" domain={[0, "auto"]} tickLine={false} axisLine={false} tickFormatter={formatearCompacto} minTickGap={24} />
        <ChartTooltip content={<ChartTooltipContent />} cursor={{ fill: "var(--muted)" }} />
        <Bar dataKey={serie.clave} fill={`var(--color-${serie.clave})`} radius={[0, 4, 4, 0]} maxBarSize={24} isAnimationActive={false}>
          {mostrarValores && <LabelList dataKey="textoValor" position="right" className="fill-foreground" fontSize={11} />}
        </Bar>
      </BarChart>
    </ChartContainer>
  );
}
