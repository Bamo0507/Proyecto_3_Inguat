"use client";

import { Bar, BarChart, CartesianGrid, LabelList, Line, LineChart, Rectangle, ReferenceDot, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { formatearCompacto, formatearNumero } from "@/features/shared/lib/formato";
import type { calendarioDiario, resumirDias } from "../lib/resumen-diario";

const formatoFecha = new Intl.DateTimeFormat("es-GT", { dateStyle: "long", timeZone: "UTC" });

export function GraficoDiario({ calendario, evento }: {
  calendario: ReturnType<typeof calendarioDiario>;
  evento: string;
}) {
  const diasEvento = calendario.filter((dia) => evento && dia.evento === evento && dia.visitantes !== null);
  return (
    <>
      <p className="mb-1 text-xs font-medium text-muted-foreground">Visitantes</p>
      <ChartContainer
        config={{ visitantes: { label: "Presencia diaria", color: "var(--chart-1)" } }}
        className="h-60 w-full"
        aria-label={evento ? `Visitantes por día del mes. Días de ${evento} destacados.` : "Visitantes por día del mes"}
      >
        <LineChart accessibilityLayer data={calendario} margin={{ top: 12, right: 12, bottom: 4, left: 0 }}>
          <CartesianGrid vertical={false} stroke="var(--border)" strokeDasharray="3 5" />
          <XAxis dataKey="fecha" tickLine={false} axisLine={false} tickFormatter={(fecha: string) => fecha.slice(-2)} minTickGap={14}
            height={44} label={{ value: "Día del mes", position: "insideBottom", fill: "var(--muted-foreground)" }} />
          <YAxis domain={[0, "auto"]} width={49} tickLine={false} axisLine={false} tickFormatter={formatearCompacto} />
          <ChartTooltip content={<ChartTooltipContent labelFormatter={(fecha) => {
            const dia = calendario.find((observacion) => observacion.fecha === fecha);
            if (!dia) return fecha;
            return (
              <>
                {formatoFecha.format(new Date(dia.fecha + "T00:00:00Z"))}
                {dia.evento && dia.evento !== "Regular" && <span className="block text-muted-foreground">{dia.evento}</span>}
              </>
            );
          }} />} />
          <Line dataKey="visitantes" type="linear" stroke="var(--color-visitantes)" strokeWidth={2.5}
            connectNulls={false} dot={{ r: 2, strokeWidth: 0, fill: "var(--color-visitantes)" }} isAnimationActive={false} />
          {diasEvento.map((dia) => (
            <ReferenceDot key={dia.fecha} x={dia.fecha} y={dia.visitantes!} r={5}
              fill="var(--chart-3)" stroke="var(--card)" strokeWidth={2} />
          ))}
        </LineChart>
      </ChartContainer>
    </>
  );
}

export function GraficoSemanal({ semana }: { semana: ReturnType<typeof resumirDias>["semana"] }) {
  const datos = semana.map((dia) => ({
    ...dia,
    etiqueta: dia.etiqueta + " · " + dia.dias,
    valorVisible: dia.promedio === null ? "" : formatearNumero(dia.promedio),
  }));
  return (
    <>
      <p className="mb-1 text-xs font-medium text-muted-foreground">Día de la semana</p>
      <ChartContainer config={{ promedio: { label: "Promedio diario", color: "var(--chart-1)" } }}
        className="h-60 w-full" aria-label="Presencia promedio de lunes a domingo. Cada etiqueta indica el número de días observados.">
        <BarChart accessibilityLayer layout="vertical" data={datos} margin={{ top: 4, right: 55, bottom: 4, left: 0 }}>
          <CartesianGrid horizontal={false} stroke="var(--border)" strokeDasharray="3 5" />
          <XAxis type="number" domain={[0, "auto"]} axisLine={false} tickLine={false} tickFormatter={formatearCompacto}
            height={44} label={{ value: "Promedio de visitantes", position: "insideBottom", fill: "var(--muted-foreground)" }} />
          <YAxis type="category" dataKey="etiqueta" axisLine={false} tickLine={false} width={91} tickMargin={8} />
          <ChartTooltip content={<ChartTooltipContent />} />
          <Bar dataKey="promedio" fill="var(--color-promedio)" maxBarSize={18} isAnimationActive={false}
            shape={(props) => <Rectangle {...props} radius={[0, 4, 4, 0]}
              fill={datos[props.index]?.finDeSemana ? "var(--chart-2)" : "var(--color-promedio)"} />}>
            <LabelList dataKey="valorVisible" position="right" offset={7} className="fill-foreground text-[11px] tabular-nums" />
          </Bar>
        </BarChart>
      </ChartContainer>
    </>
  );
}
