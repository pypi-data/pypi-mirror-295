import numpy as np
import h5py
import xml.etree.ElementTree as ET

def create_image_headers(metadata, num_images):
    # Definir la estructura del ImageHeader según el estándar ISMRM
    # Esta es una versión simplificada, ajusta según tus necesidades específicas
    header_dtype = np.dtype([
        ('version', '<h'),
        ('flags', '<q'),
        ('measurement_uid', '<i'),
        ('matrix_size', '<h', 3),
        ('field_of_view', '<f', 3),
        ('channels', '<h'),
        ('position', '<f', 3),
        ('read_dir', '<f', 3),
        ('phase_dir', '<f', 3),
        ('slice_dir', '<f', 3),
        ('patient_table_position', '<f', 3),
        ('average', '<h'),
        ('slice', '<h'),
        ('contrast', '<h'),
        ('phase', '<h'),
        ('repetition', '<h'),
        ('set', '<h'),
        ('acquisition_time_stamp', '<i'),
        ('physiology_time_stamp', '<i', 3),
        ('image_type', '<h'),
        ('image_index', '<h'),
        ('image_series_index', '<h'),
        ('user_int', '<i', 8),
        ('user_float', '<f', 8)
    ])

    headers = np.zeros(num_images, dtype=header_dtype)

    for i in range(num_images):
        headers[i]['version'] = 1
        headers[i]['flags'] = 1  # Ajusta según sea necesario
        headers[i]['measurement_uid'] = 1  # Ajusta según sea necesario
        headers[i]['matrix_size'] = metadata['AcquisitionMatrix']
        headers[i]['field_of_view'] = metadata['FOV']
        headers[i]['channels'] = metadata['NumberOfChannels']
        # Ajusta los siguientes campos según tus datos específicos
        headers[i]['position'] = [0, 0, i * metadata['SliceThickness']]
        headers[i]['read_dir'] = [1, 0, 0]
        headers[i]['phase_dir'] = [0, 1, 0]
        headers[i]['slice_dir'] = [0, 0, 1]
        headers[i]['patient_table_position'] = [0, 0, 0]
        headers[i]['average'] = 0
        headers[i]['slice'] = i
        headers[i]['contrast'] = 0
        headers[i]['phase'] = 0
        headers[i]['repetition'] = 0
        headers[i]['set'] = 0
        headers[i]['acquisition_time_stamp'] = 0
        headers[i]['physiology_time_stamp'] = [0, 0, 0]
        headers[i]['image_type'] = 1  # Ajusta según sea necesario
        headers[i]['image_index'] = i
        headers[i]['image_series_index'] = 0

    return headers

def convertir_a_h5(rawdata, metadata, nombre_archivo_h5, xml_header, waveforms=None, config=None, config_file=None):
    if not nombre_archivo_h5.endswith('.h5'):
        nombre_archivo_h5 += '.h5'
    
    with h5py.File(nombre_archivo_h5, 'w') as h5_file:
        # /dataset/xml
        h5_file.create_dataset('/dataset/xml', data=xml_header.encode('utf-8'))
        
        # /dataset/data
        h5_file.create_dataset('/dataset/data', data=rawdata)
        
        # /dataset/waveforms
        if waveforms is not None:
            h5_file.create_dataset('/dataset/waveforms', data=waveforms)
        
        # /dataset/image_0/data
        image_group = h5_file.create_group('/dataset/image_0')
        # Aquí deberías usar tu función de reconstrucción real
        image_data = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(rawdata, axes=(-2, -1)), axes=(-2, -1)), axes=(-2, -1))
        image_group.create_dataset('data', data=np.abs(image_data), dtype=np.float32)
        
        # /dataset/image_0/header
        num_images = image_data.shape[0]  # Asumiendo que la primera dimensión es el número de imágenes
        image_headers = create_image_headers(metadata, num_images)
        image_group.create_dataset('header', data=image_headers)
        
        # /dataset/image_0/attributes
        image_meta = ET.Element('ImageMetaAttributes')
        for key, value in metadata.items():
            meta_tag = ET.SubElement(image_meta, key)
            meta_tag.text = str(value)
        image_meta_str = ET.tostring(image_meta, encoding='utf-8', method='xml')
        image_group.create_dataset('attributes', data=image_meta_str)
        
        # /dataset/config
        if config is not None:
            h5_file.create_dataset('/dataset/config', data=config.encode('utf-8'))
        
        # /dataset/config_file
        if config_file is not None:
            h5_file.create_dataset('/dataset/config_file', data=config_file.encode('utf-8'))
    
    print(f"Archivo HDF5 guardado exitosamente como {nombre_archivo_h5}")


def generate_xml_header(metadata):
    root = ET.Element("ismrmrdHeader")
    encoding = ET.SubElement(root, "encoding")
    
    # Agregar los metadatos específicos
    parameters = ET.SubElement(encoding, "parameters")
    for key, value in metadata.items():
        param = ET.SubElement(parameters, key)
        if isinstance(value, tuple):
            for i, v in enumerate(value):
                ET.SubElement(param, f"value{i+1}").text = str(v)
        else:
            ET.SubElement(param, "value").text = str(value)

    return ET.tostring(root, encoding='unicode', method='xml')