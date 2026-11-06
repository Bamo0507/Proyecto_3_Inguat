"use client";

import { useId, useState, type ReactNode } from "react";
import { CalendarDays } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { SelectorBuscable } from "@/components/ui/selector-buscable";
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { GraficoLineas } from "@/features/shared/components/grafico-lineas";
import { PanelGrafico } from "@/features/shared/components/panel-grafico";
import { formatearNumero, formatearPorcentaje } from "@/features/shared/lib/formato";
import { calendarioDiario, nombreMes, nombreMunicipio, resumirDias } from "../lib/resumen-diario";
import { origenes, type DiaObservado, type MunicipioTemporal, type Origen, type SerieMunicipal } from "../types";
import { GraficoDiario, GraficoSemanal } from "./graficos-diarios";

const seriesMensuales = [
  { clave: "observado", nombre: "Observado", color: "var(--chart-1)" },
  { clave: "estimado", nombre: "Estimado", color: "var(--chart-3)", discontinua: true },
];

const fechaCorta = new Intl.DateTimeFormat("es-GT", { day: "numeric", month: "long", timeZone: "UTC" });

function Selector<Valor extends string>({ etiqueta, valor, cambiar, opciones }: {
  etiqueta: string;
  valor: Valor;
  cambiar: (valor: Valor) => void;
  opciones: { value: Valor; label: string }[];
}) {
  const id = useId();

  return (
    <div className="flex min-w-0 flex-col gap-1.5">
      <label htmlFor={id} className="text-xs font-medium text-muted-foreground">{etiqueta}</label>
      <Select items={opciones} value={valor}
        onValueChange={(opcion) => { if (opcion !== null) cambiar(opcion); }}>
        <SelectTrigger id={id} className="w-full cursor-pointer data-[size=default]:h-11">
          <SelectValue>
            <span className="line-clamp-2 min-w-0 whitespace-normal leading-tight">
              {opciones.find((opcion) => opcion.value === valor)?.label}
            </span>
          </SelectValue>
        </SelectTrigger>
        <SelectContent align="start" alignItemWithTrigger={false} side="bottom" sideOffset={6}
          className="min-w-56 max-w-[calc(100vw-2rem)]">
          <SelectGroup>
            {opciones.map(({ value, label }) => (
              <SelectItem key={value} value={value} className="min-h-9 [&>span:first-child]:min-w-0">
                <span className="whitespace-normal">{label}</span>
              </SelectItem>
            ))}
          </SelectGroup>
        </SelectContent>
      </Select>
    </div>
  );
}

function BloqueDiario({ dias, mes, calendario, evento }: {
  dias: DiaObservado[];
  mes: string;
  calendario: ReturnType<typeof calendarioDiario>;
  evento: string;
}) {
  const resumen = resumirDias(dias, evento);
  const diasSinBase = resumen.semana.filter((dia) => !dia.dias).map((dia) => dia.etiqueta.toLowerCase());
  const maximoDiario = dias.reduce<DiaObservado | undefined>(
    (maximo, dia) => !maximo || dia.visitantes > maximo.visitantes ? dia : maximo, undefined,
  );
  const maximoSemanal = resumen.semana.reduce<(typeof resumen.semana)[number] | undefined>(
    (maximo, dia) => dia.promedio !== null && (!maximo || dia.promedio > (maximo.promedio ?? 0)) ? dia : maximo,
    undefined,
  );
  const variacion = resumen.variacion;

  return (
    <>
      <div className="grid min-w-0 gap-4 lg:grid-cols-2">
        <PanelGrafico nivelTitulo="h3" titulo="¿En qué fechas hubo más visitantes?"
          descripcion={maximoDiario
            ? `Mayor registro el ${fechaCorta.format(new Date(maximoDiario.fecha + "T00:00:00Z"))} · ${formatearNumero(maximoDiario.visitantes)} visitantes`
            : undefined}
          estado={dias.length ? "listo" : "vacio"}>
          <GraficoDiario calendario={calendario} evento={evento} />
          {evento && (
            <p className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
              <span aria-hidden="true" className="size-2.5 shrink-0 rounded-full bg-chart-3" />
              Días de {evento}
            </p>
          )}
        </PanelGrafico>
        <PanelGrafico nivelTitulo="h3" titulo="¿Qué días de la semana reciben más visitantes?"
          descripcion="Solo días sin eventos. El número junto a cada día indica cuántas fechas se promediaron.">
          {resumen.diasRegulares ? (
            <>
              <GraficoSemanal semana={resumen.semana} />
              {maximoSemanal?.promedio != null && (
                <p className="mt-2 text-xs text-muted-foreground">
                  {maximoSemanal.etiqueta} · mayor promedio diario con {formatearNumero(maximoSemanal.promedio)} visitantes.
                </p>
              )}
              {diasSinBase.length > 0 && <p className="text-xs text-muted-foreground">Sin dato para {diasSinBase.join(", ")}.</p>}
            </>
          ) : (
            <p className="grid h-60 place-items-center px-4 text-center text-sm text-muted-foreground">
              {dias.length ? "Los días con datos coinciden con eventos. El promedio semanal necesita días sin eventos." : "Este mes no tiene datos para esta selección."}
            </p>
          )}
        </PanelGrafico>
      </div>

      {evento && (
        <div className="grid gap-3 rounded-xl border border-border bg-card px-4 py-3 sm:grid-cols-2 lg:grid-cols-[1.5fr_repeat(3,minmax(0,1fr))] lg:items-center">
          <div>
            <h3 className="flex items-center gap-2 text-sm font-semibold">
              <span aria-hidden="true" className="size-2.5 shrink-0 rounded-full bg-chart-3" />
              {evento}
            </h3>
            <p className="mt-0.5 text-xs text-muted-foreground">
              {resumen.diasEvento} {resumen.diasEvento === 1 ? "día resaltado" : "días resaltados"} en {nombreMes(mes).toLowerCase()}
            </p>
          </div>
          <DatoResumen etiqueta="Frente a los días sin eventos del mismo mes" destacar>
            {variacion === null ? "Sin comparación disponible"
              : variacion === 0 ? "El mismo promedio"
                : `${formatearPorcentaje(Math.abs(variacion))} ${variacion > 0 ? "más" : "menos"} por día`}
          </DatoResumen>
          <DatoResumen etiqueta="Visitantes por día de evento">
            {resumen.promedioEvento === null ? "Sin dato" : formatearNumero(resumen.promedioEvento)}
          </DatoResumen>
          <DatoResumen etiqueta={`Visitantes por día sin eventos · ${resumen.diasRegulares} días`}>
            {resumen.promedioRegular === null ? "Sin dato" : formatearNumero(resumen.promedioRegular)}
          </DatoResumen>
        </div>
      )}
      <p className="text-pretty text-xs leading-relaxed text-muted-foreground">
        Las fechas de cada evento provienen de la fuente de datos. Los gráficos por procedencia usan registros con país identificado.
      </p>
    </>
  );
}

function DatoResumen({ etiqueta, children, destacar }: {
  etiqueta: string;
  children: ReactNode;
  destacar?: boolean;
}) {
  return (
    <dl className="min-w-0">
      <dt className="text-xs leading-snug text-muted-foreground">{etiqueta}</dt>
      <dd className={`mt-1 text-sm font-semibold tabular-nums ${destacar ? "text-primary" : ""}`}>{children}</dd>
    </dl>
  );
}

function BloqueMensual({ serie, origen }: { serie: SerieMunicipal; origen: Origen }) {
  const datos = serie.meses.map((mes) => ({
    etiqueta: nombreMes(mes.fecha, true),
    observado: mes.tipo === "Observado" ? mes.visitantes : null,
    estimado: mes.tipo === "Estimado" ? mes.visitantes : null,
  }));
  const validacion = serie.validacion;
  return (
    <PanelGrafico nivelTitulo="h3" titulo={origen} descripcion="Visitantes por mes" className="[&_[data-slot=chart]]:h-64 sm:[&_[data-slot=chart]]:h-72">
      <div className="mb-2 grid grid-cols-3 gap-2 rounded-lg bg-muted/55 px-3 py-2.5">
        {serie.meses.filter((mes) => mes.tipo === "Estimado").map((mes) => (
          <DatoResumen key={mes.fecha} etiqueta={nombreMes(mes.fecha) + " · estimado"} destacar>
            {formatearNumero(mes.visitantes)}
          </DatoResumen>
        ))}
        <DatoResumen etiqueta="Error promedio al probar el modelo">
          {validacion ? `${formatearNumero(validacion.mae)} visitantes por mes` : "Sin dato"}
        </DatoResumen>
      </div>
      <GraficoLineas datos={datos} series={seriesMensuales} ejeHorizontal="Mes y año" ejeVertical="Visitantes"
        descripcionAccesible={`${origen}. Visitantes por mes. Enero y febrero de 2026 son estimaciones.`} />
    </PanelGrafico>
  );
}

export function DinamicaTemporal({ municipios }: { municipios: MunicipioTemporal[] }) {
  const eventoId = useId();
  const [municipio, cambiarMunicipio] = useState(municipios[0].nombre);
  const [origen, cambiarOrigen] = useState<Origen>("Nacionales");
  const meses = Array.from(new Set(municipios.flatMap(({ series }) =>
    origenes.flatMap((origen) => series[origen].dias.map((dia) => dia.fecha.slice(0, 7)))))).sort();
  const [mes, cambiarMes] = useState(meses.includes("2025-12") ? "2025-12" : meses[0]);
  const { series } = municipios.find(({ nombre }) => nombre === municipio)!;
  const dias = series[origen].dias.filter((dia) => dia.fecha.startsWith(mes + "-"));
  const eventos = Array.from(new Set(dias.filter((dia) => dia.evento !== "Regular").map((dia) => dia.evento)));
  const [eventoElegido, cambiarEvento] = useState("");
  const evento = eventos.includes(eventoElegido) ? eventoElegido : eventos[0] ?? "";
  const calendario = calendarioDiario(dias, mes);
  const diasDelMes = calendario.length;
  const parcial = dias.length < diasDelMes;

  return (
    <div className="flex min-w-0 flex-col gap-7 py-6 sm:py-7">
      <div className="rounded-xl bg-card p-3 ring-1 ring-foreground/10 md:p-4">
        <div className="grid gap-3 sm:grid-cols-2">
          <SelectorBuscable etiqueta="Municipio" valor={municipio} cambiar={cambiarMunicipio}
            opciones={municipios.map(({ nombre }) => ({ value: nombre, label: nombreMunicipio(nombre) }))} />
          <Selector etiqueta="Procedencia" valor={origen} cambiar={cambiarOrigen}
            opciones={origenes.map((opcion) => ({ value: opcion, label: opcion }))} />
        </div>
        <p className="mt-2.5 text-xs text-muted-foreground">
          Municipio y procedencia se aplican a todos los gráficos.
        </p>
      </div>

      <section aria-labelledby="detalle-diario" className="flex min-w-0 flex-col gap-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h2 id="detalle-diario" className="flex items-center gap-2 text-balance text-2xl font-medium tracking-tight">
              <CalendarDays aria-hidden="true" className="size-5 shrink-0 text-primary" /> El mes, día por día
            </h2>
            <p className="mt-1 text-sm text-muted-foreground">{nombreMunicipio(municipio)} · {origen} · {nombreMes(mes)}</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant={parcial ? "outline" : "secondary"}>{parcial ? "Cobertura parcial" : "Mes completo"}</Badge>
            <span className="text-xs text-muted-foreground">{dias.length} de {diasDelMes} días con datos</span>
          </div>
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <SelectorBuscable etiqueta="Mes y año" valor={mes} cambiar={cambiarMes}
            opciones={meses.map((opcion) => ({ value: opcion, label: nombreMes(opcion) }))} />
          {eventos.length > 1 ? (
            <SelectorBuscable etiqueta="Evento destacado" valor={evento} cambiar={cambiarEvento}
              opciones={eventos.map((nombre) => ({ value: nombre, label: nombre }))} />
          ) : (
            <div className="flex min-w-0 flex-col gap-1.5">
              <label htmlFor={eventoId} className="text-xs font-medium text-muted-foreground">Evento destacado</label>
              <input id={eventoId} type="text" readOnly value={evento || "Sin eventos registrados"}
                className="h-11 w-full min-w-0 rounded-lg border border-border bg-popover px-2.5 text-sm text-popover-foreground focus-visible:outline-2 focus-visible:outline-ring" />
            </div>
          )}
        </div>
        <BloqueDiario dias={dias} mes={mes} calendario={calendario} evento={evento} />
      </section>

      <section aria-labelledby="estimaciones-mensuales" className="flex min-w-0 flex-col gap-4 border-t border-border pt-6">
        <div>
          <h2 id="estimaciones-mensuales" className="text-balance text-2xl font-medium tracking-tight">Visitas observadas y estimadas</h2>
          <p className="mt-1 text-sm text-muted-foreground">{nombreMunicipio(municipio)} · {origen} · septiembre de 2025 a agosto de 2026</p>
        </div>
        <BloqueMensual serie={series[origen]} origen={origen} />
        <p className="max-w-3xl text-pretty text-xs leading-relaxed text-muted-foreground">
          Enero y febrero muestran estimaciones. Para calcular el error, se compararon las estimaciones de mayo y junio de 2026
          con los registros de esos meses. La cifra indica cuántos visitantes por mes separaron, en promedio, las estimaciones de los registros.
          {origen === "Nacionales" && " Para estimar las visitas nacionales se usaron las entradas al país como referencia indirecta."}
        </p>
      </section>
    </div>
  );
}
