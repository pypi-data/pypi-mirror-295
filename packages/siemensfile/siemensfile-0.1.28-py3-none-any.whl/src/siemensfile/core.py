import sys
import os

# Añadir la carpeta 'src' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import os
import numpy as np
import pandas as pd
from twixtools.twixtools import read_twix
from siemensfile.siemensfile import extraer_metadata_recursivamente
from siemensfile.reconstruction import reconstruct_image

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