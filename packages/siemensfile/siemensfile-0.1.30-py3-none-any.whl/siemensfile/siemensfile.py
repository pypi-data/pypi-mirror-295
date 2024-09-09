import sys
import os
import numpy as np

import traceback
# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from siemensfile.utils import *
from siemensfile.reconstruction import reconstruct_image_NoCartesiana


def lectura_twix(ruta_archivo):
    carpeta_destino = setup_output_folder(ruta_archivo)
    nombre_base = os.path.splitext(os.path.basename(ruta_archivo))[0]
    print(f"Iniciando lectura_twix con archivo: {ruta_archivo}")
    print(f"Carpeta de destino: {carpeta_destino}")
    print(f"Nombre base del archivo: {nombre_base}")
    
    try:
        twix, datos = read_twix_file(ruta_archivo)
        scan = select_scan(twix)
        
        print('\nProcesando el espacio seleccionado:')
        print('TR = %d ms' % (scan['hdr']['Phoenix']['alTR'][0] / 1000))
        print('TE = %d ms' % (scan['hdr']['Phoenix']['alTE'][0] / 1000))
        
        image_mdbs = extract_image_data(scan)
        kspace = create_kspace(image_mdbs)
        image_ifft = reconstruct_image(kspace)
        
        visualize_kspace(kspace, carpeta_destino, nombre_base)
        visualize_reconstruction(image_ifft, carpeta_destino, nombre_base)
        
        image_ifft_final = final_reconstruction(kspace)
        
        metadatos = prepare_metadata(scan, kspace.shape[2])
        save_dicom(image_ifft_final, metadatos, carpeta_destino, nombre_base)

        # Exportar metadatos a JSON
        json_output_path = os.path.join(carpeta_destino, f"{nombre_base}_metadata.json")
        export_metadata_to_json(datos, json_output_path)

        #         # Exportar a formato HDF5 (MRD)
        # h5_output_path = os.path.join(carpeta_destino, f"{nombre_base}_mrd.h5")
        # xml_header = generate_xml_header(datos)
        # convertir_a_h5(kspace, datos, h5_output_path, xml_header)
        
        print(f"\nRuta temporal: {carpeta_destino}")
        print(f"Archivos generados: {os.listdir(carpeta_destino)}")
    except Exception as e:
        print(f"Error al procesar el archivo twix: {str(e)}")
        print(f"Error detallado: {traceback.format_exc()}")

    return datos, kspace

def siemensfile(file_path, reconstruccion="Cartesiana"):
    reconstruccion = reconstruccion.lower()
    if reconstruccion == "cartesiana":
        metadata, kspace = lectura_twix(file_path)
        return metadata, kspace
    elif reconstruccion == "nocartesiana":
        print(f"El método de reconstrucción '{reconstruccion}' no está implementado.")
        reconstruct_image_NoCartesiana(file_path, method="NoCartesiana")
    else:
        print(f"El método de reconstrucción '{reconstruccion}' no está implementado.")
    return None