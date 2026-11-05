"use client";

import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import { formatearPorcentaje } from "@/features/shared/lib/formato";
import type { ResumenSeleccion } from "./calculos";

const config: ChartConfig = {
  paso: { label: "De paso", color: "var(--chart-1)" },
  pernocta: { label: "Con pernocta", color: "var(--chart-2)" },
};

export function GraficoComposicion({ datos }: { datos: ResumenSeleccion["composicion"] }) {
  const barras = datos.map((r) => ({ origen: r.origen, paso: r.paso === null ? 0 : r.paso * 100, pernocta: r.pernocta === null ? 0 : r.pernocta * 100 }));
  return (
    <div className="space-y-4">
      <ChartContainer config={config} className="h-48 w-full" aria-label="Porcentajes de visitas de paso y con pernocta, calculados dentro de cada origen">
        <BarChart accessibilityLayer data={barras} layout="vertical" margin={{ top: 10, right: 14, bottom: 4, left: 12 }}>
          <CartesianGrid horizontal={false} stroke="var(--border)" strokeDasharray="3 5" />
          <YAxis type="category" dataKey="origen" width={92} tickLine={false} axisLine={false} />
          <XAxis type="number" domain={[0, 100]} ticks={[0, 25, 50, 75, 100]} tickFormatter={(v: number) => `${v}%`} tickLine={false} axisLine={false} />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Bar dataKey="paso" stackId="composicion" fill="var(--color-paso)" isAnimationActive={false} />
          <Bar dataKey="pernocta" stackId="composicion" fill="var(--color-pernocta)" radius={[0, 4, 4, 0]} isAnimationActive={false} />
        </BarChart>
      </ChartContainer>
      <div className="grid gap-2 sm:grid-cols-2">
        {datos.map((r) => <div key={r.origen} className="rounded-md border border-border bg-muted/40 px-3 py-2 text-sm leading-relaxed">
          <strong className="block text-foreground">{r.origen}</strong>
          {r.paso === null ? <span className="text-muted-foreground">Sin visitas registradas; proporción no calculable.</span> : <span>
            <span className="font-medium text-primary">De paso: {formatearPorcentaje(r.paso, 1)}</span>
            <span className="mx-2 text-muted-foreground" aria-hidden="true">·</span>
            <span className="font-medium text-chart-2">Con pernocta: {formatearPorcentaje(r.pernocta ?? 0, 1)}</span>
          </span>}
        </div>)}
      </div>
    </div>
  );
}
