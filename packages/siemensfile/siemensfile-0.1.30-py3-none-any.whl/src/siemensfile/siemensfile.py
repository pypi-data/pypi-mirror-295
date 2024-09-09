import sys
import os

# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from twixtools.twixtools import read_twix
import numpy as np
import os
import pandas as pd
import shutil
import traceback
from siemensfile.utils import *
from siemensfile.reconstruction import reconstruct_image


def lectura_twix(ruta_archivo):
    carpeta_destino = os.path.join(os.path.dirname(__file__), "output")
    if os.path.exists(carpeta_destino):
        shutil.rmtree(carpeta_destino)
    os.makedirs(carpeta_destino)
    
    try:
        twix = read_twix(ruta_archivo, parse_pmu=False)
        datos = []
        for i, scan in enumerate(twix):
            hdr = scan['hdr']
            metadata_planos = extraer_metadata_recursivamente(hdr)
            datos.append(metadata_planos)

        df = pd.DataFrame(datos)
        nombre_archivo_json = os.path.join(carpeta_destino, 'datos_twix.json')
        df.to_json(nombre_archivo_json, index=False)
        print(f'Datos guardados exitosamente en {nombre_archivo_json}')

        print('\nNúmero de escaneos separados (multi-raid):', len(twix))
        for i, scan in enumerate(twix):
            print(f'\nProcesando Scan {i+1}:')
            try:
                print('TR = %d ms\n' % (scan['hdr']['Phoenix']['alTR'][0] / 1000))

                image_mdbs = [mdb for mdb in scan['mdb'] if mdb.is_image_scan()]
                if not image_mdbs:
                    print(f"No se encontraron escaneos de imagen válidos para el Scan {i+1}. No se puede reconstruir la imagen.")
                    continue

                n_line = 1 + max([mdb.cLin for mdb in image_mdbs])
                n_channel, n_column = image_mdbs[0].data.shape
                kspace = np.zeros([n_line, n_channel, n_column], dtype=np.complex64)
                for mdb in image_mdbs:
                    if mdb.cLin < n_line and mdb.data.shape == (n_channel, n_column):
                        kspace[mdb.cLin] = mdb.data
                print('Forma del espacio k:', kspace.shape)

                # Guardar imagen del espacio k
                save_image(kspace[:, 0]**0.2, 
                           os.path.join(carpeta_destino, f'espacio_k_scan_{i+1}.png'),
                           f'Espacio K - Scan {i+1}',
                           'Datos crudos antes de la reconstrucción')

                # Reconstrucción IFFT (Cartesiana)
                image_ifft = ifftnd(kspace, [0, -1])
                image_ifft = rms_comb(image_ifft)
                save_image(image_ifft, 
                           os.path.join(carpeta_destino, f'reconstruccion_cartesiana_ifft_scan_{i+1}.png'),
                           f'Reconstrucción Cartesiana (IFFT) - Scan {i+1}',
                           'Transformada inversa de Fourier rápida')

                print(f"Imágenes guardadas para el Scan {i+1}")
            except Exception as e:
                print(f"Error procesando Scan {i+1}: {str(e)}")
                traceback.print_exc()

        print(f"Procesamiento completado. Resultados guardados en {carpeta_destino}")
    except Exception as e:
        print(f"Error al leer el archivo twix: {str(e)}")
        traceback.print_exc()

    return os.path.abspath(carpeta_destino)


def siemensfile(file_path, reconstruction=None):
    try:
        twix = read_twix(file_path, parse_pmu=False)
        metadata = []
        rawdata = []

        for i, scan in enumerate(twix):
            hdr = scan['hdr']
            metadata_planos = extraer_metadata_recursivamente(hdr)
            metadata.append(metadata_planos)

            image_mdbs = [mdb for mdb in scan['mdb'] if mdb.is_image_scan()]
            if image_mdbs:
                n_line = 1 + max([mdb.cLin for mdb in image_mdbs])
                n_channel, n_column = image_mdbs[0].data.shape
                kspace = np.zeros([n_line, n_channel, n_column], dtype=np.complex64)
                for mdb in image_mdbs:
                    if mdb.cLin < n_line and mdb.data.shape == (n_channel, n_column):
                        kspace[mdb.cLin] = mdb.data
                rawdata.append(kspace)

        if reconstruction:
            reconstruct_image(rawdata, reconstruction)

        return metadata, rawdata

    except Exception as e:
        print(f"Error processing SIEMENS file: {str(e)}")
        return None, None
    