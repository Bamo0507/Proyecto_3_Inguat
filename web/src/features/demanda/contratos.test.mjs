/** Ejecutar desde web/: node --test src/features/demanda/contratos.test.mjs */
import assert from "node:assert/strict";
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { createRequire } from "node:module";
import { test, after } from "node:test";
import ts from "typescript";

const require = createRequire(import.meta.url);
const temporal = mkdtempSync(path.join(tmpdir(), "demanda-test-"));
for (const archivo of ["decimal", "tipos", "calculos", "datos"]) {
  const origen = new URL(`./${archivo}.ts`, import.meta.url);
  const compilado = ts.transpileModule(readFileSync(origen, "utf8"), { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, esModuleInterop: true } });
  writeFileSync(path.join(temporal, `${archivo}.js`), compilado.outputText);
}
after(() => rmSync(temporal, { recursive: true, force: true }));
const { prepararDatosDemanda, leerCsv } = require(path.join(temporal, "datos.js"));
const { calcularSeleccion } = require(path.join(temporal, "calculos.js"));
const { comparar, sumar } = require(path.join(temporal, "decimal.js"));
const csv = readFileSync(new URL("../../../../data/processed/movilidad_mensual/movilidad_mensual_atitlan.csv", import.meta.url), "utf8");
const datos = prepararDatosDemanda(csv);

function cerca(real, esperado, tolerancia = 0.00001) { assert.ok(Math.abs(real - esperado) < tolerancia, `${real} != ${esperado}`); }

test("lector CSV respeta campos citados y comillas escapadas", () => {
  assert.deepEqual(leerCsv('a,b\n"Costa, Rica","país ""citado"""\n'), [["a", "b"], ["Costa, Rica", 'país "citado"']]);
});

test("aritmética decimal conserva diferencias menores que un entero", () => {
  assert.equal(sumar("0.1", "0.2"), "0.3");
  assert.equal(comparar("2820.000000000000001", "2820"), 1);
});

test("Panajachel septiembre 2025 concilia indicadores y ranking", () => {
  const r = calcularSeleccion(datos, "Panajachel", "2025-09", "Extranjeros");
  cerca(r.visitasMes, 10273.41328405376772);
  cerca(r.promedioMensual, 18923.883061929820646);
  cerca(r.diasPersona, 14730.45398967257951);
  cerca(r.estadia, 2.249290685296583);
  assert.equal(r.mesesConDato, 10);
  assert.equal(r.ranking[0].pais, "Estados Unidos");
  assert.equal(r.ranking[0].visitas, "2820");
  assert.equal(r.serie.length, 12);
  assert.deepEqual(r.serie.filter((x) => x.visitas === null).map((x) => x.mes), ["2026-01", "2026-02"]);
});

test("mes cambia detalle, no el promedio; composición usa dos bases", () => {
  const septiembre = calcularSeleccion(datos, "Panajachel", "2025-09", "Extranjeros");
  const octubre = calcularSeleccion(datos, "Panajachel", "2025-10", "Extranjeros");
  assert.equal(septiembre.promedioMensual, octubre.promedioMensual);
  assert.notEqual(septiembre.visitasMes, octubre.visitasMes);
  for (const r of septiembre.composicion) cerca(r.paso + r.pernocta, 1);
});

test("selector local no entra en ranking ni composición", () => {
  const extranjeros = calcularSeleccion(datos, "Panajachel", "2025-09", "Extranjeros");
  const nacionales = calcularSeleccion(datos, "Panajachel", "2025-09", "Nacionales");
  assert.deepEqual(extranjeros.ranking, nacionales.ranking);
  assert.deepEqual(extranjeros.composicion, nacionales.composicion);
  assert.notEqual(extranjeros.visitasMes, nacionales.visitasMes);
});

test("cobertura y país desconocido se conservan sin asignar un origen", () => {
  assert.equal(datos.resumenes.length, 200);
  assert.equal(datos.desconocidos.reduce((total, fila) => total + fila.registros, 0), 25);
  assert.ok(datos.mercados.every((fila) => fila.pais !== "Guatemala" && fila.pais !== "\\N"));
  for (const municipio of datos.municipios) {
    for (const origen of ["Nacionales", "Extranjeros"]) {
      assert.equal(datos.resumenes.filter((fila) => fila.municipio === municipio && fila.origen === origen).length, 10);
    }
  }
});

test("denominador cero produce proporción y estadía no definidas", () => {
  const muestra = { ...datos, resumenes: [{ municipio: "X", mes: "2025-09", origen: "Nacionales", visitas: "0", diasPersona: "0", visitasPaso: "0", visitasPernocta: "0", diasPernocta: "0" }], mercados: [], desconocidos: [], mesesObservados: ["2025-09"] };
  const r = calcularSeleccion(muestra, "X", "2025-09", "Nacionales");
  assert.equal(r.estadia, null);
  assert.equal(r.composicion[0].paso, null);
  assert.equal(r.visitasMes, 0);
});
