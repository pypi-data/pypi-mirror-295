import numpy as np
from fileformats.core import extra_implementation
from fileformats.medimage import DwiEncoding
from fileformats.medimage_mrtrix3 import BFile


@extra_implementation(DwiEncoding.read_array)
def bfile_read_array(bfile: BFile) -> np.ndarray:
    return np.asarray(
        [[float(x) for x in ln.split()] for ln in bfile.read_contents().splitlines()]
    )
