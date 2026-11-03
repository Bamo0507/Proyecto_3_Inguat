"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FirmaAgua } from "@/components/firma-agua";
import { SiluetaAtitlan } from "@/components/silueta-atitlan";
import { FondoAgua } from "@/components/fondo-agua";
import { modulos } from "@/lib/modulos";
import { cn } from "@/lib/utils";

export function EstructuraObservatorio({ children }: { children: React.ReactNode }) {
  const ruta = usePathname();

  return (
    <div className="observatorio flex min-h-svh flex-col">
      <a href="#contenido" className="skip-link">Saltar al contenido</a>
      <header className="border-t-4 border-primary bg-card">
        <div className="mx-auto flex max-w-[1680px] flex-wrap items-center justify-between gap-4 px-6 py-4 sm:px-10 lg:px-16 lg:py-5">
          <Link href="/demanda" aria-label="Atitlán, inicio del observatorio" className="inline-flex items-center gap-4 rounded-sm">
            <SiluetaAtitlan className="size-10 shrink-0 fill-primary/10 stroke-primary stroke-[2] lg:size-12" />
            <span className="text-[1.9rem] leading-none font-medium tracking-[-0.055em] lg:text-[2.25rem]">Atitlán<span className="text-primary">.</span></span>
            <span className="hidden border-l border-border pl-4 text-xs leading-relaxed text-muted-foreground sm:inline">Observatorio turístico</span>
          </Link>
          <div className="hidden items-center gap-4 sm:flex" aria-label="Lago de Atitlán, departamento de Sololá, Guatemala">
            <div className="flex items-baseline gap-3">
              <span className="text-xs font-medium tracking-wide text-muted-foreground">Guatemala</span>
              <span aria-hidden="true" className="text-border">/</span>
              <span className="text-base font-semibold tracking-tight">Sololá</span>
            </div>
          </div>
        </div>
      </header>

      <div className="sticky top-0 z-20 border-y border-border bg-card">
        <nav aria-label="Módulos del observatorio" className="mx-auto grid max-w-[1680px] grid-cols-2 px-4 sm:px-8 md:grid-cols-4 lg:px-14">
          {modulos.map((modulo, indice) => {
            const activo = ruta === modulo.ruta;
            return (
              <Link key={modulo.ruta} href={modulo.ruta} aria-current={activo ? "page" : undefined}
                className={cn("module-nav group relative isolate flex min-h-20 flex-col justify-center gap-1.5 overflow-hidden border-b border-border px-3 py-3 md:min-h-20 md:border-b-0 md:px-5 md:py-4", activo ? "text-primary-foreground" : "text-foreground")}>
                <FirmaAgua className="module-waves absolute top-1/2 -right-10 z-[-1] hidden size-28 -translate-y-1/2 stroke-[0.8] xl:block" />
                <span className="flex items-center gap-3">
                  <span className="module-index font-mono text-[11px]">{String(indice + 1).padStart(2, "0")}</span>
                  <span className="text-sm leading-snug font-medium tracking-tight lg:text-base">{modulo.nombre}</span>
                </span>
                <span className="module-detail pl-7 text-xs leading-relaxed">{modulo.detalle}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="workspace-surface flex flex-1 flex-col">
      <FondoAgua />
      <main id="contenido" tabIndex={-1} className="observatorio-main mx-auto flex w-full max-w-[1680px] flex-1 flex-col outline-none">{children}</main>
      </div>

    </div>
  );
}
