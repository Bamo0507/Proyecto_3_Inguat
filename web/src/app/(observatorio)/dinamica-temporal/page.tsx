import type { Metadata } from "next";
import { connection } from "next/server";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { PaginaModulo } from "@/components/pagina-modulo";
import { DinamicaTemporal } from "@/features/dinamica-temporal/components/dinamica-temporal";
import { cargarDinamicaTemporal } from "@/features/dinamica-temporal/lib/cargar-datos";
import { modulos } from "@/lib/modulos";

export const metadata: Metadata = {
  title: modulos[1].nombre + " · Atitlán",
  description: modulos[1].descripcion,
};

export default async function Page() {
  await connection();
  const municipios = await cargarDinamicaTemporal().catch((error: unknown) => {
    console.error("Dinámica temporal", error);
    return null;
  });
  return (
    <PaginaModulo indice={1}>
      {municipios ? <DinamicaTemporal municipios={municipios} /> : (
        <Alert variant="destructive" className="my-8">
          <AlertTitle>No se pudieron cargar los datos de dinámica temporal</AlertTitle>
          <AlertDescription>Vuelve a cargar la página o inténtalo más tarde.</AlertDescription>
        </Alert>
      )}
    </PaginaModulo>
  );
}
