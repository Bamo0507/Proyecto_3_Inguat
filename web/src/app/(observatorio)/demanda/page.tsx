import type { Metadata } from "next";
import { connection } from "next/server";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { PaginaModulo } from "@/components/pagina-modulo";
import { VistaDemanda } from "@/features/demanda/vista-demanda";
import { cargarDatosDemanda } from "@/features/demanda/datos";
import type { DatosDemanda } from "@/features/demanda/tipos";
import { modulos } from "@/lib/modulos";

export const metadata: Metadata = {
  title: `${modulos[0].nombre} · Atitlán`,
  description: modulos[0].descripcion,
};

export default async function Page() {
  await connection();
  let datos: DatosDemanda | null = null;
  try {
    datos = await cargarDatosDemanda();
  } catch (error) {
    console.error("No se pudo preparar la demanda mensual", error);
  }
  return <PaginaModulo indice={0}>{datos ? <VistaDemanda datos={datos} /> : <Alert variant="destructive" className="my-8"><AlertTitle>No se pudieron cargar los datos de demanda</AlertTitle><AlertDescription>Vuelve a intentar más tarde. Si el problema continúa, verifica que esté disponible la tabla procesada de movilidad mensual.</AlertDescription></Alert>}</PaginaModulo>;
}
