"""Regresiones de la politica de nulos y conservacion de filas departamentales."""
import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'src'))
from config import COLUMNAS_SALIDA
from utils import leer, limpiar_cantidad


def cargar_etapa(fuente):
    spec = importlib.util.spec_from_file_location(f'tipado_{fuente}', RAIZ / 'src' / fuente / '03_tipado.py')
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class PoliticaDeCantidades(unittest.TestCase):
    def test_decimales_conservan_precision_y_distinguen_ausencia_de_invalidez(self):
        valores = pd.Series(['0', '0.7900', 'NULL', '1.01', 'texto', 'Infinity'], dtype='string')
        incidencias = []
        resultado = limpiar_cantidad(valores, 'indice_ocupacion', incidencias, pd.Series(range(20, 26)), maximo=1)
        self.assertEqual(resultado.iloc[:2].tolist(), ['0', '0.7900'])
        self.assertTrue(resultado.iloc[2:].isna().all())
        self.assertEqual(incidencias[0]['clasificacion'], 'ausente_en_origen')
        self.assertEqual([i['valor_original'] for i in incidencias], ['NULL', '1.01', 'texto', 'Infinity'])
        self.assertEqual([i['fila_csv'] for i in incidencias], [22, 23, 24, 25])

    def test_ocupacion_rechaza_cantidades_sin_perder_meses(self):
        etapa = cargar_etapa('ocupacion_hotelera')
        entrada = leer('ocupacion_hotelera', '02_seleccion')
        entrada.loc[0, 'indice_ocupacion'] = '1.20'
        entrada.loc[1, 'indice_ocupacion'] = 'invalido'
        entrada.loc[2, 'indice_ocupacion'] = 'NULL'
        salidas, evidencia = {}, []
        with patch.object(etapa, 'leer', return_value=entrada.copy()), \
             patch.object(etapa, 'guardar', side_effect=lambda df, fuente, nombre: salidas.update({nombre: df.copy()})), \
             patch.object(etapa, 'guardar_incidencias_cantidad', side_effect=lambda fuente, registros: evidencia.extend(registros)):
            etapa.main()
        final = salidas['ocupacion_solola']
        self.assertEqual(len(final), 36)
        self.assertEqual(final.columns.tolist(), COLUMNAS_SALIDA['ocupacion_hotelera'])
        self.assertTrue(final.loc[:2, 'indice_ocupacion'].isna().all())
        self.assertEqual(len(evidencia), 3)
        self.assertEqual(evidencia[0]['valor_original'], '1.20')
        self.assertEqual(evidencia[2]['clasificacion'], 'ausente_en_origen')
        self.assertTrue(all(i['fila_csv'] >= 2 for i in evidencia))

    def test_oferta_rechaza_cantidades_y_solo_senala_incoherencias_de_capacidad(self):
        etapa = cargar_etapa('oferta_alojamiento')
        entrada = leer('oferta_alojamiento', '02_seleccion')
        entrada.loc[0, 'habitaciones'] = 'dos'
        entrada.loc[1, 'plazas_cama'] = '1.5'
        entrada.loc[2, 'establecimientos'] = '-1'
        entrada.loc[3, 'habitaciones'] = '0'
        salidas, evidencia = {}, []
        with patch.object(etapa, 'leer', return_value=entrada.copy()), \
             patch.object(etapa, 'guardar', side_effect=lambda df, fuente, nombre: salidas.update({nombre: df.copy()})), \
             patch.object(etapa, 'guardar_incidencias_cantidad', side_effect=lambda fuente, registros: evidencia.extend(registros)):
            etapa.main()
        final = salidas['oferta_solola']
        self.assertEqual(len(final), 15)
        self.assertTrue(pd.isna(final.loc[0, 'habitaciones']))
        self.assertTrue(pd.isna(final.loc[1, 'plazas_cama']))
        self.assertTrue(pd.isna(final.loc[2, 'establecimientos']))
        self.assertEqual(final.loc[3, 'habitaciones'], 0)
        self.assertEqual(sum(i['clasificacion'] == 'rechazado_por_invalido' for i in evidencia), 3)
        self.assertTrue(any(i['clasificacion'] == 'requiere_revision' and i['valor_normalizado'] == '0' for i in evidencia))

    def test_fecha_invalida_impide_publicar_ocupacion(self):
        etapa = cargar_etapa('ocupacion_hotelera')
        entrada = leer('ocupacion_hotelera', '02_seleccion')
        entrada.loc[0, 'mes'] = '13'
        with patch.object(etapa, 'leer', return_value=entrada), \
             patch.object(etapa, 'filas_origen', return_value=pd.Series(range(2, 38))), \
             patch.object(etapa, 'guardar') as guardar:
            with self.assertRaises(ValueError):
                etapa.main()
            guardar.assert_not_called()


if __name__ == '__main__':
    unittest.main()
