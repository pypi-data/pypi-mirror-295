import sys
import os

# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
import numpy as np
import shutil
from unittest.mock import patch
from twixtools.twixtools import read_twix
from siemensfile.utils import ifftnd, rms_comb, extraer_metadata_recursivamente, save_image
from siemensfile.siemensfile import lectura_twix

class TestSIEMENSFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ruta_archivo = os.path.join(os.path.dirname(__file__), "datatest", "siemens_file_test_cartesian_sample.dat")

    def test_ifftnd(self):
        kspace = np.zeros((4, 4), dtype=np.complex64)
        kspace[0, 0] = 1.0 + 1.0j
        result = ifftnd(kspace)
        print("Resultado de ifftnd:", result)
        self.assertEqual(result.shape, (4, 4))
        print("Valor en [2, 0]:", np.abs(result[2, 0]))
        self.assertAlmostEqual(np.abs(result[0, 0]), 0.3535533905932738, places=7)

    def test_ifftnd_2d(self):
        kspace = np.zeros((4, 4), dtype=np.complex64)
        kspace[0, 0] = 1.0
        result = ifftnd(kspace, axes=[0, 1])
        self.assertEqual(result.shape, (4, 4))
        # Verificar que todos los valores tienen la misma magnitud
        self.assertTrue(np.allclose(np.abs(result), 0.25, atol=1e-7))
        # Verificar que la suma de los valores absolutos al cuadrado es cercana a 1
        self.assertAlmostEqual(np.sum(np.abs(result)**2), 1.0, places=7)

    def test_ifftnd_complex(self):
        kspace = np.zeros((8, 8), dtype=np.complex64)
        kspace[0, 0] = 1 + 1j
        kspace[0, 1] = 1 - 1j
        result = ifftnd(kspace)
        # Verificar que el resultado tiene valores complejos
        self.assertFalse(np.allclose(result.imag, 0, atol=1e-7))
        # Verificar que la suma de los valores absolutos al cuadrado es igual a la entrada
        input_energy = np.sum(np.abs(kspace)**2)
        output_energy = np.sum(np.abs(result)**2)
        self.assertAlmostEqual(output_energy, input_energy, places=6)  # Reducimos la precisión a 6 decimales
        # Verificar que la energía total es cercana a 4 (2^2 + 2^2)
        self.assertAlmostEqual(output_energy, 4.0, places=6)  # Reducimos la precisión a 6 decimales
        # Verificar que la diferencia relativa entre energías es pequeña
        relative_error = abs(output_energy - input_energy) / input_energy
        self.assertLess(relative_error, 1e-6)  # Permitimos un error relativo de hasta 0.0001%

    def test_rms_comb(self):
        sig = np.array([[1.0, 2.0], [3.0, 4.0]])
        result = rms_comb(sig, axis=1)
        self.assertEqual(result.shape, (2,))
        self.assertAlmostEqual(result[0], 1.5811388300841898, places=7)
        self.assertAlmostEqual(result[1], 3.5355339059327378, places=7)

    def test_rms_comb_3d(self):
        sig = np.ones((2, 3, 4))
        result = rms_comb(sig, axis=2)
        self.assertEqual(result.shape, (2, 3))
        self.assertAlmostEqual(result[0, 0], 1.0, places=7)

    def test_rms_comb_invalid_axis(self):
        sig = np.array([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            rms_comb(sig, axis=2)  # Invalid axis

    def test_extraer_metadata_recursivamente(self):
        hdr = {
            'Phoenix': {
                'alTR': [2000],
                'alTE': [30]
            },
            'Meas': {
                'TE': 30
            }
        }
        result = extraer_metadata_recursivamente(hdr)
        expected = {
            'Phoenix.alTR': [2000],
            'Phoenix.alTE': [30],
            'Meas.TE': 30
        }
        self.assertDictEqual(result, expected)
    def test_extraer_metadata_recursivamente_nested(self):
        hdr = {
            'level1': {
                'level2': {
                    'key': 'value'
                }
            },
            'another_key': 42
        }
        result = extraer_metadata_recursivamente(hdr)
        self.assertEqual(result['level1.level2.key'], 'value')
        self.assertEqual(result['another_key'], 42)

    def test_save_image(self):
        data = np.random.rand(4, 4)
        filename = "test_image.png"
        save_image(data, filename, "Test Image")
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

    def test_save_image_with_subtitle(self):
        data = np.random.rand(10, 10)
        filename = "test_image_subtitle.png"
        save_image(data, filename, "Test Title", "Test Subtitle")
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

    def test_lectura_twix(self):
        if os.path.exists(self.ruta_archivo):
            result_dir = lectura_twix(self.ruta_archivo)
            self.assertTrue(os.path.exists(result_dir))
            self.assertTrue(os.path.exists(os.path.join(result_dir, 'datos_twix.json')))
            self.assertTrue(os.path.exists(os.path.join(result_dir, 'espacio_k_scan_1.png')))
            self.assertTrue(os.path.exists(os.path.join(result_dir, 'reconstruccion_cartesiana_ifft_scan_1.png')))
            print(f"Imágenes guardadas en: {result_dir}")
            shutil.rmtree(result_dir)
        else:
            self.fail(f"Archivo de prueba no encontrado: {self.ruta_archivo}")

    @patch('siemensfile.siemensfile.read_twix')
    def test_lectura_twix_mocked(self, mock_read_twix):
        mock_scan = {
            'hdr': {'Phoenix': {'alTR': [2000]}},
            'mdb': []
        }
        mock_read_twix.return_value = [mock_scan]
        with patch('builtins.print') as mock_print:
            result = lectura_twix("mock_file.dat")
            self.assertTrue(os.path.exists(result))
            self.assertTrue(os.path.exists(os.path.join(result, 'datos_twix.json')))
            mock_print.assert_any_call("No se encontraron escaneos de imagen válidos para el Scan 1. No se puede reconstruir la imagen.")
        shutil.rmtree(result)

if __name__ == '__main__':
    unittest.main()