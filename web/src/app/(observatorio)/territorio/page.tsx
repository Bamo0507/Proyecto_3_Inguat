import type { Metadata } from "next";
import { modulos } from "@/lib/modulos";
import { PaginaModulo } from "@/components/pagina-modulo";

export const metadata: Metadata = {
  title: `${modulos[3].nombre} · Atitlán`,
  description: modulos[3].descripcion,
};

export default function Page() {
  return <PaginaModulo indice={3} />;
}
