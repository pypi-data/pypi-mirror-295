import sys
import os

# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import matplotlib.pyplot as plt
import numpy as np
from siemensfile.utils import ifftnd, rms_comb

def reconstruct_image(rawdata, method="Cartesiana"):
    if method.lower() == "cartesiana":
        fig, axs = plt.subplots(len(rawdata), 2, figsize=(10, 5*len(rawdata)))
        for i, kspace in enumerate(rawdata):
            # Espacio K
            axs[i, 0].imshow(np.abs(kspace[:, 0])**0.2, cmap='gray')
            axs[i, 0].set_title(f'Espacio K - Scan {i+1}')
            
            # Reconstrucción IFFT
            image_ifft = ifftnd(kspace, [0, -1])
            image_ifft = rms_comb(image_ifft)
            axs[i, 1].imshow(np.abs(image_ifft), cmap='gray')
            axs[i, 1].set_title(f'Reconstrucción IFFT - Scan {i+1}')

        plt.tight_layout()
        plt.show()
    else:
        print(f"Método de reconstrucción '{method}' no implementado.")