"use client";

import { useId, type ReactNode } from "react";
import { CircleAlert, ChartNoAxesCombined } from "lucide-react";
import { Card, CardAction, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { EstadoVisual } from "../types/graficos";

type PanelGraficoProps = {
  titulo: string;
  descripcion?: string;
  acciones?: ReactNode;
  pie?: ReactNode;
  children: ReactNode;
  estado?: EstadoVisual;
  mensajeError?: string;
  onReintentar?: () => void;
  className?: string;
};

export function PanelGrafico({ titulo, descripcion, acciones, pie, children, estado = "listo", mensajeError = "No fue posible cargar esta visualización.", onReintentar, className }: PanelGraficoProps) {
  const id = useId();
  return (
    <Card className={cn("min-w-0", className)} role="region" aria-labelledby={id} aria-busy={estado === "cargando"}>
      <CardHeader className="gap-y-2">
        <CardTitle><h2 id={id}>{titulo}</h2></CardTitle>
        {descripcion && <CardDescription>{descripcion}</CardDescription>}
        {acciones && <CardAction>{acciones}</CardAction>}
      </CardHeader>
      <CardContent className="min-w-0">
        {estado === "cargando" ? (
          <div className="flex h-80 flex-col justify-end gap-4" role="status">
            <span className="sr-only">Cargando visualización</span>
            <Skeleton className="h-60 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        ) : estado === "vacio" ? (
          <Empty className="h-80">
            <EmptyHeader>
              <EmptyMedia variant="icon"><ChartNoAxesCombined /></EmptyMedia>
              <EmptyTitle>No hay datos para mostrar</EmptyTitle>
              <EmptyDescription>Prueba con otro período o ajusta la selección.</EmptyDescription>
            </EmptyHeader>
          </Empty>
        ) : estado === "error" ? (
          <div className="flex h-80 flex-col justify-center gap-4">
            <Alert variant="destructive"><CircleAlert /><AlertTitle>No se pudo mostrar el gráfico</AlertTitle><AlertDescription>{mensajeError}</AlertDescription></Alert>
            {onReintentar && <Button variant="outline" onClick={onReintentar} className="self-start">Reintentar</Button>}
          </div>
        ) : children}
      </CardContent>
      {pie && <CardFooter><div className="text-xs leading-relaxed text-muted-foreground">{pie}</div></CardFooter>}
    </Card>
  );
}
