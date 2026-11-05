/** Aritmética decimal exacta para sumar y ordenar las cantidades del CSV. */
type Decimal = { entero: bigint; escala: number };

function leer(valor: string): Decimal {
  if (!/^-?\d+(?:\.\d+)?$/.test(valor)) throw new Error(`Cantidad decimal inválida: ${valor}`);
  const negativo = valor.startsWith("-");
  const [parteEntera, fraccion = ""] = (negativo ? valor.slice(1) : valor).split(".");
  const entero = BigInt(parteEntera + fraccion) * (negativo ? BigInt(-1) : BigInt(1));
  return { entero, escala: fraccion.length };
}

function alinear(a: Decimal, b: Decimal): [bigint, bigint, number] {
  const escala = Math.max(a.escala, b.escala);
  return [a.entero * BigInt(10) ** BigInt(escala - a.escala), b.entero * BigInt(10) ** BigInt(escala - b.escala), escala];
}

function escribir({ entero, escala }: Decimal): string {
  const negativo = entero < BigInt(0) ? "-" : "";
  const digitos = (entero < BigInt(0) ? -entero : entero).toString().padStart(escala + 1, "0");
  if (!escala) return negativo + digitos;
  const fraccion = digitos.slice(-escala).replace(/0+$/, "");
  return negativo + digitos.slice(0, -escala) + (fraccion ? `.${fraccion}` : "");
}

export function sumar(a: string, b: string): string {
  const [x, y, escala] = alinear(leer(a), leer(b));
  return escribir({ entero: x + y, escala });
}

export function comparar(a: string, b: string): number {
  const [x, y] = alinear(leer(a), leer(b));
  return x < y ? -1 : x > y ? 1 : 0;
}

export function numero(valor: string): number { return Number(valor); }

/** Divide sin redondear la cantidad de origen; la conversión a Number ocurre solo al presentar. */
export function cociente(a: string, b: string): number | null {
  const x = leer(a);
  const y = leer(b);
  if (y.entero === BigInt(0)) return null;
  return Number(x.entero * BigInt(10) ** BigInt(y.escala)) / Number(y.entero * BigInt(10) ** BigInt(x.escala));
}

export function techo(valor: string): string {
  const x = leer(valor);
  const divisor = BigInt(10) ** BigInt(x.escala);
  const entero = x.entero / divisor;
  return (x.entero > BigInt(0) && x.entero % divisor !== BigInt(0) ? entero + BigInt(1) : entero).toString();
}
