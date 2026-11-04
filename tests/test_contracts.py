"""Contrastes de salidas con evidencia cuantitativa de los notebooks."""
import csv
import hashlib
import unittest
from decimal import Decimal
from pathlib import Path

RAIZ=Path(__file__).resolve().parents[1]
RAW=RAIZ/'data'/'raw'
PROCESSED=RAIZ/'data'/'processed'


def tabla(fuente,nombre):
    with (PROCESSED/fuente/f'{nombre}.csv').open(newline='',encoding='utf-8') as archivo:
        return list(csv.DictReader(archivo))


class Contratos(unittest.TestCase):
    def test_mensual(self):
        original=tabla('movilidad_mensual','01_ingesta')
        final=tabla('movilidad_mensual','movilidad_mensual_atitlan')
        self.assertEqual(len(final),9860)
        self.assertEqual(list(final[0]),['destino','anio','mes','pais','es_consecutivo','fecha','visitantes','dias_persona'])
        self.assertEqual(sum(f['pais']==r'\N' for f in final),25)
        self.assertEqual(sum(f['es_consecutivo']=='mayor a 1 dia' and Decimal(o['permanencia_prom'])==1 for f,o in zip(final,original) if o['permanencia_prom']),778)
        self.assertEqual(sum(f['visitantes']=='0.0' and f['dias_persona']=='0.0' for f in final),13)
        for f,o in zip(final,original):
            self.assertEqual(Decimal(f['visitantes']),Decimal(o['visitantes']))
            self.assertEqual(Decimal(f['dias_persona']),Decimal(o['dias_persona']))
        self.assertFalse(any(f['anio']=='2026' and f['mes'] in {'1','2'} for f in final))

    def test_diaria(self):
        original=tabla('movilidad_diaria','01_ingesta')
        final=tabla('movilidad_diaria','movilidad_diaria_atitlan')
        self.assertEqual(len(final),82952)
        self.assertEqual(len(final[0]),9)
        self.assertEqual(sum(f['pais']==r'\N' for f in final),41)
        self.assertEqual(sum(o['pais']=='ESPAÃ±A' and f['pais']=='ESPAÑA' for o,f in zip(original,final)),1376)
        self.assertEqual(sum(Decimal(f['cantidad_visitantes'])==0 for f in final),100)
        self.assertTrue(any(f['fecha' if 'fecha' in f else 'idfecha'].startswith('2025-12-29') and f['num_semana']=='1' for f in final))
        for f,o in zip(final,original): self.assertEqual(Decimal(f['cantidad_visitantes']),Decimal(o['cantidad_visitantes']))

    def test_migracion(self):
        fuente=tabla('migracion','01_ingesta')
        seleccion=tabla('migracion','02_seleccion')
        detalle=tabla('migracion','migracion_detalle')
        mensual=tabla('migracion','migracion_mensual')
        incidencias=tabla('migracion','incidencias')
        notas=tabla('migracion','01_notas')
        self.assertEqual((len(fuente),len(seleccion),len(detalle),len(mensual)),(161036,132894,132894,210))
        self.assertEqual(len(notas),10)
        self.assertTrue(any('USO EXCLUSIVAMENTE ACADÉMICO' in n['descripcion'] for n in notas))
        self.assertEqual(sum(r['Tipo de Viajero'] in {'Turista','Excursionista'} for r in fuente),137642)
        self.assertEqual(len(detalle[0]),13)
        self.assertEqual(sum(i['motivo']=='catalogo_frontera' for i in incidencias),92)
        self.assertEqual(sum(i['motivo']=='colision_conocida_conservada' for i in incidencias),40)
        self.assertTrue(all(i['fila_excel'].isdigit() for i in incidencias))
        self.assertEqual(sum(d['region_dos']==r'\N' for d in detalle),13)
        self.assertEqual(sum(d['regiones_omt']==r'\N' for d in detalle),5)
        self.assertTrue(all(Decimal(a['Viajero'])==Decimal(b['viajeros']) for a,b in zip(seleccion,detalle)))
        self.assertEqual(sum(m['viajeros']==r'\N' for m in mensual),5)
        self.assertTrue(all(m['viajeros']==r'\N' for m in mensual if '2020-04-01'<=m['fecha']<='2020-08-01'))
        self.assertEqual((sum(m['conjunto']=='ajuste' for m in mensual),sum(m['conjunto']=='evaluacion' for m in mensual)),(36,6))
        self.assertEqual(sum(Decimal(d['viajeros']) for d in detalle),sum(Decimal(m['viajeros']) for m in mensual if m['viajeros']!=r'\N'))

    def test_departamentales(self):
        ocup=tabla('ocupacion_hotelera','ocupacion_solola')
        oferta=tabla('oferta_alojamiento','oferta_solola')
        self.assertEqual((len(ocup),len(oferta)),(36,15))
        self.assertEqual(list(ocup[0]),['fecha','indice_ocupacion'])
        self.assertTrue(all(Decimal(0)<=Decimal(r['indice_ocupacion'])<=Decimal(1) for r in ocup))
        self.assertEqual(len({r['fecha'] for r in ocup}),36)
        self.assertEqual({(r['anio'],r['trimestre']) for r in oferta},{('2022','4'),('2023','4'),('2024','4'),('2025','4'),('2026','1')})
        self.assertEqual(len({(r['anio'],r['trimestre'],r['tipo_alojamiento']) for r in oferta}),15)

    def test_fuentes_intactas(self):
        esperadas={
            'BD_moviidad_mensual.xlsx':'e518da912823a711b2423bac7bb32a0f61d8f74311399103fb30c4458cd2d356',
            'BD_moviidad_diario.xlsx':'b5760b52e3154dc3629f70e6fbb004e61a79190b99871c549682dd56728b23d7',
            'Base_Migracion_2009-2026jun.xlsx':'cdaba77918ae889c847ba8459503f9cce2441efac41b3d3aa0f05ac9ab283846',
            'indice_ocupacion_mensual_2023_2025_1.csv':'ea6b5c823cbe0fa18e387b581f4b9df7f4a0fb05eaf8b1c04ea473334cd52c14',
            'oferta_hotelera_2022_2026.csv':'bda9caf5184b088406abfdc37019d1483bd640e3ae08fe07e76d2b9b6c6b6fa8',
        }
        for nombre,esperada in esperadas.items():
            with self.subTest(nombre=nombre): self.assertEqual(hashlib.sha256((RAW/nombre).read_bytes()).hexdigest(),esperada)

if __name__=='__main__': unittest.main()
