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