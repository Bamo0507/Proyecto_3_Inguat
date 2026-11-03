import type { Metadata } from "next";
import { modulos } from "@/lib/modulos";
import { PaginaModulo } from "@/components/pagina-modulo";

export const metadata: Metadata = {
  title: `${modulos[1].nombre} · Atitlán`,
  description: modulos[1].descripcion,
};

export default function Page() {
  return <PaginaModulo indice={1} />;
}
