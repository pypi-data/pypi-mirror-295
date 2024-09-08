import sys
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from twixtools.twixtools import read_twix
import numpy as np
import os
import pandas as pd
import shutil
import traceback
from siemensfile.utils import *
from siemensfile.reconstruction import reconstruct_image_NoCartesiana
from pydicom.data import get_testdata_file


def lectura_twix(ruta_archivo):
    """
    Función para leer un archivo TWIX, extraer los datos de imagen,
    guardarlos en el espacio k y reconstruir las imágenes usando IFFT.
    """
    carpeta_base = os.path.dirname(ruta_archivo)
    carpeta_destino = os.path.join(carpeta_base, "output")
    
    print(f"Iniciando lectura_twix con archivo: {ruta_archivo}")
    print(f"Carpeta de destino: {carpeta_destino}")
    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    print(f"Nombre base del archivo: {nombre_base}")

    # Asegurarse de que la carpeta de destino exista o crearla
    if os.path.exists(carpeta_destino):
        shutil.rmtree(carpeta_destino)
    os.makedirs(carpeta_destino)
    print(f"Carpeta de destino creada/limpiada: {carpeta_destino}")
    
    try:
        print("Intentando leer el archivo twix...")
        twix = read_twix(ruta_archivo, parse_pmu=False)
        print(f"Archivo twix leído exitosamente. Número de escaneos: {len(twix)}")
        datos = []
        for i, scan in enumerate(twix):
            hdr = scan['hdr']
            metadata_planos = extraer_metadata_recursivamente(hdr)
            datos.append(metadata_planos)

        # Seleccionar el espacio a procesar
        if len(twix) > 1:
            scan = twix[1]  # Usar el segundo espacio si está disponible
            print('Procesando el segundo espacio')
        else:
            scan = twix[0]  # Usar el primer (y único) espacio si solo hay uno
            print('Procesando el único espacio disponible')

        print('\nProcesando el segundo espacio:')
        print('TR = %d ms' % (scan['hdr']['Phoenix']['alTR'][0] / 1000))
        print('TE = %d ms' % (scan['hdr']['Phoenix']['alTE'][0] / 1000))

        image_mdbs = [mdb for mdb in scan['mdb'] if mdb.is_image_scan()]
        if not image_mdbs:
            raise ValueError("No se encontraron escaneos de imagen válidos en el segundo espacio")

        print(f"Número de escaneos de imagen encontrados: {len(image_mdbs)}")

        n_line = 1 + max([mdb.cLin for mdb in image_mdbs])
        n_channel, n_column = image_mdbs[0].data.shape
        n_slice = 1 + max([mdb.cSlc for mdb in image_mdbs])
        print(f"Dimensiones: n_line={n_line}, n_channel={n_channel}, n_column={n_column}, n_slice={n_slice}")

        kspace = np.zeros([n_line, n_channel, n_column, n_slice], dtype=np.complex64)
        for mdb in image_mdbs:
            if mdb.cLin < n_line and mdb.cSlc < n_slice and mdb.data.shape == (n_channel, n_column):
                kspace[mdb.cLin, :, :, mdb.cSlc] = mdb.data
        print('k-space shape', kspace.shape)

        # Reconstrucción IFFT
        print("Realizando reconstrucción IFFT...")
        image_ifft = ifftnd(kspace, [0, 2])
        image_ifft = rms_comb(image_ifft, axis=1)
        print(f"Forma de la imagen reconstruida: {image_ifft.shape}")

        # Visualización
        print("Generando visualización...")
        n_rows = int(np.ceil(np.sqrt(n_slice)))
        n_cols = int(np.ceil(n_slice / n_rows))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 4*n_rows))
        axes = axes.flatten() if n_slice > 1 else [axes]

        for i in range(n_slice):
            # Espacio k
            k_abs = np.abs(kspace[:, 0, :, i])
            vmin_k = np.min(k_abs[k_abs > 0])
            vmax_k = np.max(k_abs)
            if vmin_k >= vmax_k:
                vmin_k = vmax_k * 0.1

            axes[i].imshow(k_abs, cmap='gray', origin='lower', norm=LogNorm(vmin=vmin_k, vmax=vmax_k))
            axes[i].set_title(f'Slice {i+1} - Espacio k')
            axes[i].axis('off')

        plt.tight_layout()
        nombre_imagen_png = f"{nombre_base}_kspace.png"
        nombre_archivo_png = os.path.join(carpeta_destino, nombre_imagen_png)
        plt.savefig(nombre_archivo_png, dpi=300, format='png')
        plt.close(fig)
        print(f"Imagen de espacio k guardada: {nombre_archivo_png}")


        # Visualización de las imágenes reconstruidas
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 4*n_rows))
        axes = axes.flatten() if n_slice > 1 else [axes]

        for i in range(n_slice):
            img_slice = np.abs(image_ifft[:, :, i])
            vmin_ifft = np.min(img_slice)
            vmax_ifft = np.max(img_slice)
            axes[i].imshow(img_slice, cmap='gray', origin='lower', vmin=vmin_ifft, vmax=vmax_ifft)
            axes[i].set_title(f'Slice {i+1} - Reconstrucción')
            axes[i].axis('off')

        plt.tight_layout()
        nombre_imagen_png = f"{nombre_base}_reconstruction.png"
        nombre_archivo_png = os.path.join(carpeta_destino, nombre_imagen_png)
        plt.savefig(nombre_archivo_png, dpi=300, format='png')
        plt.show()
        print(f"Imagen de reconstrucción guardada: {nombre_archivo_png}")
        print('k-space shape', kspace.shape)

        # Reconstrucción IFFT
        print("Realizando reconstrucción IFFT...")
        # Aplicar IFFT en las dimensiones de fila y columna
        image_ifft = np.fft.ifftshift(np.fft.ifft2(kspace, axes=(0, 2)), axes=(0, 2))
        
        # Combinar canales (RMS)
        image_ifft = np.sqrt(np.sum(np.abs(image_ifft)**2, axis=1))
        
        # Reorganizar para que los cortes estén en la primera dimensión
        image_ifft = np.transpose(image_ifft, (2, 0, 1))
        
        print(f"Forma de la imagen reconstruida: {image_ifft.shape}")

        # Visualización
        print("Generando visualización...")
        n_slice = image_ifft.shape[0]
        n_rows = int(np.ceil(np.sqrt(n_slice)))
        n_cols = int(np.ceil(n_slice / n_rows))
        
    # Preparar metadatos para DICOM
        metadatos = {
            'fecha': datetime.datetime.now().strftime('%Y%m%d'),
            'tipo_adquisicion': scan['hdr']['Phoenix'].get('tProtocolName', 'Unknown'),
            'TR': scan['hdr']['Phoenix']['alTR'][0] / 1000,
            'TE': scan['hdr']['Phoenix']['alTE'][0] / 1000,
            'resolucion_espacial': scan['hdr']['Phoenix'].get('sSliceArray.asSlice[0].dReadoutFOV', 250) / n_column,
            'fov': (scan['hdr']['Phoenix'].get('sSliceArray.asSlice[0].dReadoutFOV', 250),
                    scan['hdr']['Phoenix'].get('sSliceArray.asSlice[0].dPhaseFOV', 250))
        }

        # Guardar todos los slices como un archivo DICOM multiframe
        nombre_dcm = f"{nombre_base}_multiframe.dcm"
        nombre_archivo_dcm = os.path.join(carpeta_destino, nombre_dcm)
        ruta_base_dcm = get_testdata_file("CT_small.dcm")
        guardar_multiframe_dicom(image_ifft, metadatos, nombre_archivo_dcm, ruta_base_dcm=ruta_base_dcm)
        print(f"\nRuta temporal: {carpeta_destino}")
        print(f"Archivos generados: {os.listdir(carpeta_destino)}")
    except Exception as e:
        print(f"Error al procesar el archivo twix: {str(e)}")
        print(f"Error detallado: {traceback.format_exc()}")

    return datos, kspace


def siemensfile(file_path, reconstruction="Cartesiana"):
   
        reconstruction =reconstruction.lower()
        if reconstruction=="cartesiana":
            metadata,kspace=lectura_twix(file_path)
            return metadata,kspace
        elif reconstruction=="nocartesiana":
            print(f"El método de reconstrucción '{reconstruction}' no está implementado.")
            reconstruct_image_NoCartesiana(file_path, method="NoCartesiana")
        else:
            print(f"El método de reconstrucción '{reconstruction}' no está implementado.")

        return None