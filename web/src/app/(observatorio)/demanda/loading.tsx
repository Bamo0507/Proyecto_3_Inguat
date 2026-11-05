import { PaginaModulo } from "@/components/pagina-modulo";
import { Skeleton } from "@/components/ui/skeleton";

export default function Loading() {
  return <PaginaModulo indice={0}><div className="space-y-6 py-8" role="status" aria-label="Cargando datos de demanda">
    <Skeleton className="h-32 w-full" />
    <div className="grid gap-4 lg:grid-cols-3"><Skeleton className="h-40" /><Skeleton className="h-40" /><Skeleton className="h-40" /></div>
    <Skeleton className="h-96 w-full" />
    <span className="sr-only">Cargando datos de demanda</span>
  </div></PaginaModulo>;
}
