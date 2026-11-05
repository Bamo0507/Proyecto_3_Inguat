"use client";

import { useMemo, useState } from "react";
import { CalendarDays, Clock3, MapPin, UsersRound } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GraficoBarras } from "@/features/shared/components/grafico-barras";
import { GraficoLineas } from "@/features/shared/components/grafico-lineas";
import { GrupoIndicadores } from "@/features/shared/components/grupo-indicadores";
import { Indicador } from "@/features/shared/components/indicador";
import { PanelGrafico } from "@/features/shared/components/panel-grafico";
import { formatearNumero } from "@/features/shared/lib/formato";
import { calcularSeleccion, etiquetaEjeMes, etiquetaMes } from "./calculos";
import { numero, techo } from "./decimal";
import { GraficoComposicion } from "./grafico-composicion";
import type { DatosDemanda, Origen } from "./tipos";

export function VistaDemanda({ datos }: { datos: DatosDemanda }) {
  const [municipio, elegirMunicipio] = useState(datos.municipios.includes("Panajachel") ? "Panajachel" : datos.municipios[0]);
  const [mes, elegirMes] = useState(datos.mesesObservados[0]);
  const [origen, elegirOrigen] = useState<Origen>("Extranjeros");
  const resultado = useMemo(() => calcularSeleccion(datos, municipio, mes, origen), [datos, municipio, mes, origen]);
  const periodo = etiquetaMes(mes);
  const cobertura = `${etiquetaMes(datos.mesesObservados[0])} a ${etiquetaMes(datos.mesesObservados.at(-1) ?? mes)}`;
  const etiquetaSeleccionada = etiquetaEjeMes(mes);
  const graficoLinea = resultado.serie.map((r) => ({ etiqueta: etiquetaEjeMes(r.mes), visitas: r.visitas }));
  const graficoRanking = resultado.ranking.map((r) => ({ etiqueta: r.pais, visitas: numero(r.visitas), textoValor: formatearNumero(Number(techo(r.visitas))) }));

  return <div className="flex flex-col gap-8 py-8 lg:gap-10 lg:py-10">
    <div className="rounded-lg border border-border bg-card px-5 py-5 shadow-xs sm:px-7">
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">Explorar el municipio</p>
          <p className="mt-1 text-sm text-muted-foreground">Elige un lugar y un mes con datos observados.</p>
        </div>
        <span className="rounded-full bg-secondary px-3 py-1 text-xs font-medium text-secondary-foreground">Fuente: movilidad mensual · INGUAT</span>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="flex flex-col gap-2 text-sm font-medium" htmlFor="demanda-municipio">
          <span className="inline-flex items-center gap-2"><MapPin className="size-4 text-primary" aria-hidden="true" /> Municipio</span>
          <select id="demanda-municipio" value={municipio} onChange={(event) => elegirMunicipio(event.target.value)} className="h-11 w-full rounded-md border border-input bg-background px-3 text-foreground outline-none focus-visible:ring-2 focus-visible:ring-ring">
            {datos.municipios.map((nombre) => <option key={nombre} value={nombre}>{nombre}</option>)}
          </select>
        </label>
        <label className="flex flex-col gap-2 text-sm font-medium" htmlFor="demanda-mes">
          <span className="inline-flex items-center gap-2"><CalendarDays className="size-4 text-primary" aria-hidden="true" /> Mes y año</span>
          <select id="demanda-mes" value={mes} onChange={(event) => elegirMes(event.target.value)} className="h-11 w-full rounded-md border border-input bg-background px-3 text-foreground outline-none focus-visible:ring-2 focus-visible:ring-ring">
            {datos.mesesObservados.map((opcion) => <option key={opcion} value={opcion}>{etiquetaMes(opcion)}</option>)}
          </select>
        </label>
      </div>
    </div>

    <section aria-label="Indicadores y evolución mensual por procedencia" className="space-y-5">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">Visitas y estadía</p>
          <h2 className="mt-1 text-xl font-medium tracking-tight sm:text-2xl">¿Cómo se comporta la demanda en {municipio}?</h2>
          <p className="mt-1 text-sm text-muted-foreground">{periodo} · {origen.toLowerCase()} · datos observados</p>
        </div>
        <div aria-label="Procedencia para indicadores y evolución" className="flex flex-col gap-2">
          <span className="text-xs font-medium text-muted-foreground">Mostrar en este bloque</span>
          <div className="flex gap-1 rounded-lg border border-border bg-card p-1">
            {(["Nacionales", "Extranjeros"] as const).map((opcion) => <Button key={opcion} type="button" size="sm" variant={origen === opcion ? "default" : "ghost"} aria-pressed={origen === opcion} onClick={() => elegirOrigen(opcion)}>{opcion}</Button>)}
          </div>
        </div>
      </div>
      <GrupoIndicadores etiqueta={`Indicadores de ${origen.toLowerCase()} en ${municipio}`}>
        <Indicador etiqueta="¿Cuántas visitas recibe en promedio cada mes?" icono={UsersRound} valor={resultado.promedioMensual === null ? null : Math.ceil(resultado.promedioMensual)} unidad="visitas/mes" periodo={`Cobertura: ${cobertura}`} descripcion={`${resultado.mesesConDato} meses con dato; el mes elegido no cambia este promedio. Visitas aproximadas al entero superior.`} />
        <Indicador etiqueta="¿Cuántos días de visita se acumularon este mes?" icono={CalendarDays} valor={resultado.diasPersona} decimales={2} unidad="días-persona" periodo={`${periodo} · ${origen.toLowerCase()}`} descripcion="Tiempo total acumulado: 10 personas durante 3 días suman 30 días-persona." />
        <Indicador etiqueta="¿Cuántos días se quedan quienes pasan la noche?" icono={Clock3} valor={resultado.estadia} decimales={2} unidad="días por visitante" periodo={`${periodo} · ${origen.toLowerCase()}`} descripcion="Solo visitas clasificadas como «mayor a 1 día»." textoSinDatos="No definida" mensajeSinDatos="No hay visitas con pernocta para calcular la estadía." />
      </GrupoIndicadores>
      <PanelGrafico titulo="¿Cómo cambia el número de visitas de un mes a otro?" descripcion={`${municipio} · ${origen.toLowerCase()} · visitas mensuales observadas. Enero y febrero de 2026 no tienen medición.`} pie="El hueco representa meses sin observación, no cero visitas. La línea reúne dos tramos de años distintos; no permite comparar el mismo mes entre años." estado={resultado.serie.some((r) => r.visitas !== null) ? "listo" : "vacio"}>
        <div className="space-y-4">
          <div className="inline-flex flex-wrap items-baseline gap-2 rounded-md border border-primary/20 bg-secondary px-3 py-2 text-sm">
            <span className="font-medium">Mes elegido: {periodo}</span>
            <span className="font-semibold tabular-nums text-primary">{resultado.visitasMes === null ? "Sin cobertura" : `${formatearNumero(Math.ceil(resultado.visitasMes))} visitas`}</span>
          </div>
          <div className="overflow-x-auto pb-1"><div className="min-w-[640px]">
            <GraficoLineas datos={graficoLinea} series={[{ clave: "visitas", nombre: "Visitas observadas", color: "var(--chart-1)" }]} descripcionAccesible={`Serie mensual de ${origen.toLowerCase()} en ${municipio}; enero y febrero de 2026 no tienen datos. ${periodo} está resaltado.`} resaltado={resultado.visitasMes === null ? undefined : { etiqueta: etiquetaSeleccionada, valor: resultado.visitasMes }} />
          </div></div>
        </div>
      </PanelGrafico>
    </section>

    <div className="grid items-start gap-6 xl:grid-cols-[minmax(0,1.15fr)_minmax(0,1fr)]">
      <PanelGrafico titulo="¿De qué países vienen más visitantes extranjeros?" descripcion={`Top 10 de países · ${municipio} · ${periodo} · visitas reportadas`} pie="Incluye ambas categorías de permanencia. El orden usa los decimales originales; los números visibles se aproximan al entero superior. No incluye Guatemala ni procedencia desconocida." estado={resultado.ranking.length ? "listo" : "vacio"}>
        <div className="overflow-x-auto pb-1"><div className="min-w-[700px]">
          <GraficoBarras datos={graficoRanking} serie={{ clave: "visitas", nombre: "Visitas", color: "var(--chart-1)" }} descripcionAccesible={`Diez países extranjeros con más visitas en ${municipio}, ${periodo}, ordenados de mayor a menor`} altura={430} anchoEtiquetas={195} mostrarValores />
        </div></div>
      </PanelGrafico>
      <PanelGrafico titulo="¿Hay más visitas de paso o con pernocta?" descripcion={`${municipio} · ${periodo} · porcentaje dentro de cada procedencia`} pie="Cada barra usa su propio total: nacionales y extranjeros no se combinan. «De paso» corresponde a menor a 1 día; «con pernocta», a mayor a 1 día. Extranjeros incluye todos los países identificados, no solo el Top 10." estado={resultado.composicion.some((r) => r.paso !== null) ? "listo" : "vacio"}>
        <GraficoComposicion datos={resultado.composicion} />
      </PanelGrafico>
    </div>
    {resultado.procedenciaDesconocida.registros > 0 && <p className="rounded-md border border-border bg-card px-4 py-3 text-sm text-muted-foreground" role="note">
      En {municipio}, {periodo}, hay {resultado.procedenciaDesconocida.registros} {resultado.procedenciaDesconocida.registros === 1 ? "registro" : "registros"} sin país identificado ({formatearNumero(Number(techo(resultado.procedenciaDesconocida.visitas)))} {techo(resultado.procedenciaDesconocida.visitas) === "1" ? "visita aproximada" : "visitas aproximadas"}). Se conservan en la fuente, pero no se asignan a nacionales ni a extranjeros y no entran en el Top 10.
    </p>}
  </div>;
}
