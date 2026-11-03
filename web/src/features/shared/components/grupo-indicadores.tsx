import type { ReactNode } from "react";

type GrupoIndicadoresProps = {
  children: ReactNode;
  etiqueta?: string;
  periodo?: string;
};

export function GrupoIndicadores({ children, etiqueta = "Indicadores", periodo }: GrupoIndicadoresProps) {
  return (
    <section aria-label={etiqueta} className="grupo-indicadores">
      {periodo && <header className="grupo-indicadores-cabecera"><p>{periodo}</p></header>}
      <div className="grupo-indicadores-contenido">{children}</div>
    </section>
  );
}
