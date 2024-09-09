import matplotlib.pyplot as plt
import pandas as pd
import json
import shutil
import sys
import os
import datetime
from matplotlib.colors import LogNorm
from pydicom.data import get_testdata_file
import pydicom
import numpy as np


# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from twixtools.twixtools import read_twix
from siemensfile.utils import *



def ifftnd(kspace, axes=None):
    from numpy.fft import fftshift, ifftshift, ifftn
    if axes is None:
        axes = range(kspace.ndim)
    elif isinstance(axes, int):
        axes = [axes]
    
    if any(ax >= kspace.ndim or ax < -kspace.ndim for ax in axes):
        raise ValueError("Invalid axis. Axis must be less than the dimensions of kspace.")

    axes = [ax if ax >= 0 else kspace.ndim + ax for ax in axes]
    
    # Aplicar ifftshift solo a los ejes especificados
    kspace_shifted = ifftshift(kspace, axes=axes)
    
    # Realizar la IFFT
    img = ifftn(kspace_shifted, axes=axes, norm="ortho")
    
    # Aplicar fftshift solo a los ejes especificados
    img = fftshift(img, axes=axes)
    
    return img


def rms_comb(sig, axis=1):
    if axis >= sig.ndim:
        raise ValueError(f"Invalid axis {axis} for array with {sig.ndim} dimensions.")
    return np.sqrt(np.mean(np.abs(sig)**2, axis=axis))

def extraer_metadata_recursivamente(hdr, prefijo=''):
    datos_planos = {}
    for clave, valor in hdr.items():
        nueva_clave = f"{prefijo}.{clave}" if prefijo else clave
        if isinstance(valor, dict):
            datos_planos.update(extraer_metadata_recursivamente(valor, nueva_clave))
        else:
            try:
                if pd.isna(valor) or valor is None:
                    valor = 'Desconocido'
                datos_planos[nueva_clave] = valor
            except:
                datos_planos[nueva_clave] = 'Valor no compatible'
    return datos_planos

def save_image(data, filename, title, subtitle=None):
    plt.figure(figsize=(8, 8))
    plt.imshow(np.abs(data), cmap='gray', origin='lower')
    plt.title(title, fontsize=14, fontweight='bold')
    if subtitle:
        plt.text(0.5, -0.05, subtitle, ha='center', va='center', transform=plt.gca().transAxes, fontsize=10)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


def guardar_multiframe_dicom(imagenes, metadatos, ruta_salida, ruta_base_dcm='base.dcm'):
    try:
        # Cargar el archivo DICOM base
        ds = pydicom.dcmread(ruta_base_dcm)

        # Actualizar metadatos
        ds.StudyDate = metadatos.get('fecha', '')
        ds.SeriesDescription = metadatos.get('tipo_adquisicion', 'Unknown')
        ds.RepetitionTime = metadatos.get('TR', 0)
        ds.EchoTime = metadatos.get('TE', 0)
        
        # Establecer dimensiones y datos de la imagen
        ds.Rows, ds.Columns = imagenes.shape[1], imagenes.shape[2]
        ds.NumberOfFrames = imagenes.shape[0]
        ds.PixelSpacing = [metadatos.get('resolucion_espacial', 1)] * 2
        ds.SliceThickness = 1.0  # Ajustar según datos reales
        ds.SpacingBetweenSlices = 1.0  # Ajustar según datos reales
        
        # Información sobre los píxeles
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0  # Unsigned
        
        # Convertir cada corte a uint16 y organizar en el array multiframe
        multiframe_data = np.zeros((imagenes.shape[0], ds.Rows, ds.Columns), dtype=np.uint16)
        
        for i in range(imagenes.shape[0]):
            imagen_slice = imagenes[i, :, :]
            imagen_min = np.min(imagen_slice)
            imagen_max = np.max(imagen_slice)
            
            if imagen_min == imagen_max:
                imagen_scaled = np.zeros_like(imagen_slice, dtype=np.uint16)
            else:
                imagen_scaled = ((imagen_slice - imagen_min) / (imagen_max - imagen_min) * 65535).astype(np.uint16)
            
            multiframe_data[i, :, :] = imagen_scaled
        
        # Asignar los datos de imagen al campo PixelData en formato multiframe
        ds.PixelData = multiframe_data.tobytes()

        # Guardar el archivo DICOM multiframe
        ds.save_as(ruta_salida)
        print(f"Archivo DICOM multiframe guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error al guardar el archivo DICOM multiframe: {str(e)}")


def setup_output_folder(ruta_archivo):
    carpeta_base = os.path.dirname(ruta_archivo)
    carpeta_destino = os.path.join(carpeta_base, "output")
    if os.path.exists(carpeta_destino):
        shutil.rmtree(carpeta_destino)
    os.makedirs(carpeta_destino)
    print(f"Carpeta de destino creada/limpiada: {carpeta_destino}")
    return carpeta_destino

def read_twix_file(ruta_archivo):
    print("Intentando leer el archivo twix...")
    twix = read_twix(ruta_archivo, parse_pmu=False)
    print(f"Archivo twix leído exitosamente. Número de escaneos: {len(twix)}")
    datos = []
    for i, scan in enumerate(twix):
        hdr = scan['hdr']
        metadata_planos = extraer_metadata_recursivamente(hdr)
        datos.append(metadata_planos)
    return twix, datos

def select_scan(twix):
    if len(twix) > 1:
        scan = twix[1]
        print('Procesando el segundo espacio')
    else:
        scan = twix[0]
        print('Procesando el único espacio disponible')
    return scan

def extract_image_data(scan):
    image_mdbs = [mdb for mdb in scan['mdb'] if mdb.is_image_scan()]
    if not image_mdbs:
        raise ValueError("No se encontraron escaneos de imagen válidos en el segundo espacio")
    print(f"Número de escaneos de imagen encontrados: {len(image_mdbs)}")
    return image_mdbs

def create_kspace(image_mdbs):
    n_line = 1 + max([mdb.cLin for mdb in image_mdbs])
    n_channel, n_column = image_mdbs[0].data.shape
    n_slice = 1 + max([mdb.cSlc for mdb in image_mdbs])
    print(f"Dimensiones: n_line={n_line}, n_channel={n_channel}, n_column={n_column}, n_slice={n_slice}")
    
    kspace = np.zeros([n_line, n_channel, n_column, n_slice], dtype=np.complex64)
    for mdb in image_mdbs:
        if mdb.cLin < n_line and mdb.cSlc < n_slice and mdb.data.shape == (n_channel, n_column):
            kspace[mdb.cLin, :, :, mdb.cSlc] = mdb.data
    print('k-space shape', kspace.shape)
    return kspace

def reconstruct_image(kspace):
    print("Realizando reconstrucción IFFT...")
    image_ifft = ifftnd(kspace, [0, 2])
    image_ifft = rms_comb(image_ifft, axis=1)
    print(f"Forma de la imagen reconstruida: {image_ifft.shape}")
    return image_ifft

def visualize_kspace(kspace, carpeta_destino, nombre_base):
    n_slice = kspace.shape[3]
    n_rows = int(np.ceil(np.sqrt(n_slice)))
    n_cols = int(np.ceil(n_slice / n_rows))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 4*n_rows))
    axes = axes.flatten() if n_slice > 1 else [axes]

    for i in range(n_slice):
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

def visualize_reconstruction(image_ifft, carpeta_destino, nombre_base):
    n_slice = image_ifft.shape[2]
    n_rows = int(np.ceil(np.sqrt(n_slice)))
    n_cols = int(np.ceil(n_slice / n_rows))
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

def final_reconstruction(kspace):
    print("Realizando reconstrucción IFFT final...")
    image_ifft = np.fft.ifftshift(np.fft.ifft2(kspace, axes=(0, 2)), axes=(0, 2))
    image_ifft = np.sqrt(np.sum(np.abs(image_ifft)**2, axis=1))
    image_ifft = np.transpose(image_ifft, (2, 0, 1))
    print(f"Forma de la imagen reconstruida final: {image_ifft.shape}")
    return image_ifft

def prepare_metadata(scan, n_column):
    return {
        'fecha': datetime.datetime.now().strftime('%Y%m%d'),
        'tipo_adquisicion': scan['hdr']['Phoenix'].get('tProtocolName', 'Unknown'),
        'TR': scan['hdr']['Phoenix']['alTR'][0] / 1000,
        'TE': scan['hdr']['Phoenix']['alTE'][0] / 1000,
        'resolucion_espacial': scan['hdr']['Phoenix'].get('sSliceArray.asSlice[0].dReadoutFOV', 250) / n_column,
        'fov': (scan['hdr']['Phoenix'].get('sSliceArray.asSlice[0].dReadoutFOV', 250),
                scan['hdr']['Phoenix'].get('sSliceArray.asSlice[0].dPhaseFOV', 250))
    }

def save_dicom(image_ifft, metadatos, carpeta_destino, nombre_base):
    nombre_dcm = f"{nombre_base}_multiframe.dcm"
    nombre_archivo_dcm = os.path.join(carpeta_destino, nombre_dcm)
    ruta_base_dcm = get_testdata_file("CT_small.dcm")
    guardar_multiframe_dicom(image_ifft, metadatos, nombre_archivo_dcm, ruta_base_dcm=ruta_base_dcm)


## Exportar metadatos a XML
def numpy_encoder(obj):
    """
    Función auxiliar para codificar tipos de NumPy en JSON.
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def export_metadata_to_json(metadata, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"Metadatos específicos exportados a JSON: {output_path}")
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {str(e)}")


