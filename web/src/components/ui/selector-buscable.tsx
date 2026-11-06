"use client";

import { useCallback, useId, useState } from "react";
import { Combobox } from "@base-ui/react/combobox";
import { Check, ChevronDown, ChevronUp, Search } from "lucide-react";
import { Button } from "@/components/ui/button";

type Opcion<Valor extends string> = { value: Valor; label: string };

function normalizar(texto: string) {
  return texto.normalize("NFD").replace(/\p{M}/gu, "").toLocaleLowerCase("es");
}

export function SelectorBuscable<Valor extends string>({ etiqueta, valor, opciones, cambiar }: {
  etiqueta: string;
  valor: Valor;
  opciones: Opcion<Valor>[];
  cambiar: (valor: Valor) => void;
}) {
  const id = useId();
  const seleccion = opciones.find((opcion) => opcion.value === valor) ?? null;
  const [bordes, cambiarBordes] = useState({ arriba: false, abajo: false });
  const medirLista = useCallback((lista: HTMLDivElement) => {
    const arriba = lista.scrollTop > 1;
    const abajo = lista.scrollHeight - lista.clientHeight - lista.scrollTop > 1;
    cambiarBordes((actual) => actual.arriba === arriba && actual.abajo === abajo ? actual : { arriba, abajo });
  }, []);
  const observarLista = useCallback((lista: HTMLDivElement | null) => {
    if (!lista) return;

    const medir = () => medirLista(lista);
    const tamano = new ResizeObserver(medir);
    const opciones = new MutationObserver(medir);
    tamano.observe(lista);
    opciones.observe(lista, { childList: true, subtree: true });
    medir();

    return () => {
      tamano.disconnect();
      opciones.disconnect();
    };
  }, [medirLista]);

  return (
    <div className="flex min-w-0 flex-col gap-1.5">
      <label htmlFor={id} className="text-xs font-medium text-muted-foreground">{etiqueta}</label>
      <Combobox.Root
        items={opciones}
        value={seleccion}
        isItemEqualToValue={(a, b) => a.value === b.value}
        filter={(opcion, consulta) => {
          const texto = normalizar(opcion.label);
          return normalizar(consulta).trim().split(/\s+/).every((palabra) => texto.includes(palabra));
        }}
        onValueChange={(opcion) => { if (opcion) cambiar(opcion.value); }}
      >
        <Combobox.Trigger id={id} render={<Button variant="outline"
          className="h-11 w-full cursor-pointer justify-between bg-popover font-normal hover:bg-popover aria-expanded:bg-popover dark:bg-popover dark:hover:bg-popover" />}>
          <span className="line-clamp-2 min-w-0 whitespace-normal text-left leading-tight">{seleccion?.label}</span>
          <ChevronDown aria-hidden="true" className="text-muted-foreground" />
        </Combobox.Trigger>
        <Combobox.Portal>
          <Combobox.Positioner side="bottom" align="start" sideOffset={6}
            className="z-50 w-(--anchor-width) min-w-56 max-w-[calc(100vw-2rem)]">
            <Combobox.Popup aria-label={`Opciones de ${etiqueta.toLocaleLowerCase("es")}`}
              className="flex max-h-(--available-height) flex-col overflow-hidden rounded-lg border border-border bg-popover text-popover-foreground shadow-md">
              <div className="group/search flex shrink-0 items-center gap-2 border-b border-border bg-popover px-3">
                <Search aria-hidden="true" className="size-4 shrink-0 text-muted-foreground group-focus-within/search:text-foreground" />
                <Combobox.Input aria-label={`Buscar en ${etiqueta.toLocaleLowerCase("es")}`} placeholder="Buscar…"
                  className="h-11 w-full min-w-0 bg-transparent text-base outline-none sm:text-sm" />
              </div>
              <Combobox.Empty>
                <p className="px-3 py-4 text-sm text-muted-foreground">Sin resultados. Prueba con otro término.</p>
              </Combobox.Empty>
              {bordes.arriba && (
                <div data-slot="combobox-scroll-up" aria-hidden="true" className="flex shrink-0 justify-center text-muted-foreground">
                  <ChevronUp className="size-4" />
                </div>
              )}
              <Combobox.List ref={observarLista} onScroll={(event) => medirLista(event.currentTarget)}
                className="max-h-57 min-h-0 overflow-y-auto overscroll-contain p-1 data-empty:hidden">
                {(opcion: Opcion<Valor>) => (
                  <Combobox.Item key={opcion.value} value={opcion}
                    className="flex min-h-11 cursor-pointer items-center justify-between gap-2 rounded-md px-2 py-1.5 text-sm outline-none data-highlighted:bg-accent data-highlighted:text-accent-foreground">
                    <span>{opcion.label}</span>
                    <Combobox.ItemIndicator><Check aria-hidden="true" className="size-4 shrink-0" /></Combobox.ItemIndicator>
                  </Combobox.Item>
                )}
              </Combobox.List>
              {bordes.abajo && (
                <div data-slot="combobox-scroll-down" aria-hidden="true" className="flex shrink-0 justify-center text-muted-foreground">
                  <ChevronDown className="size-4" />
                </div>
              )}
            </Combobox.Popup>
          </Combobox.Positioner>
        </Combobox.Portal>
      </Combobox.Root>
    </div>
  );
}
