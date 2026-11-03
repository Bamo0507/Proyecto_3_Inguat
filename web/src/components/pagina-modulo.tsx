import { modulos } from "@/lib/modulos";

export function PaginaModulo({ indice }: { indice: number }) {
  const modulo = modulos[indice];
  return (
    <section aria-labelledby="titulo-modulo" className="module-page flex flex-1 flex-col px-6 sm:px-10 lg:px-16">
      <div className="module-introduction relative flex flex-col justify-center gap-3 border-b border-border py-8 lg:h-40 lg:py-0">
        <h1 id="titulo-modulo" className="max-w-6xl text-3xl leading-[1.08] font-medium tracking-[-0.04em] sm:text-4xl xl:text-[3.4rem]">{modulo.titulo}</h1>
        <p className="max-w-4xl text-sm leading-relaxed text-muted-foreground lg:text-base">{modulo.descripcion}</p>
      </div>
      <div className="min-h-64 flex-1" />
    </section>
  );
}
