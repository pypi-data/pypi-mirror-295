import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

import pydicom
from pydicom.dataset import Dataset, FileDataset
import datetime
import numpy as np
import os

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