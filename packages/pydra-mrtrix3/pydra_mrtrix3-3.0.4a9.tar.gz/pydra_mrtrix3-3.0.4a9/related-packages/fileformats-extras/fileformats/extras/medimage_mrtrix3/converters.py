from fileformats.core import converter
from fileformats.medimage.base import MedicalImage

from fileformats.medimage_mrtrix3 import (
    ImageFormat as MrtrixImage,
    ImageHeader as MrtrixImageHeader,
    ImageFormatGz as MrtrixImageGz,
)

try:
    from pydra.tasks.mrtrix3.v3_0 import MrConvert
except ImportError:
    from pydra.tasks.mrtrix3.latest import mrconvert as MrConvert

    in_out_file_kwargs = {"in_file": "input", "out_file": "output"}
else:
    in_out_file_kwargs = {}


@converter(
    source_format=MedicalImage,
    target_format=MrtrixImageGz,
    out_ext=MrtrixImageGz.ext,
    **in_out_file_kwargs,
)
@converter(
    source_format=MedicalImage,
    target_format=MrtrixImageHeader,
    out_ext=MrtrixImageHeader.ext,
    **in_out_file_kwargs,
)
@converter(
    source_format=MedicalImage,
    target_format=MrtrixImage,
    out_ext=MrtrixImage.ext,
    **in_out_file_kwargs,
)
def mrconvert(name, out_ext: str, **kwargs):
    """Initiate an MRConvert task with the output file extension set

    Parameters
    ----------
    name : str
        name of the converter task
    out_ext : str
        extension of the output file, used by MRConvert to determine the desired format

    Returns
    -------
    pydra.ShellCommandTask
        the converter task
    """
    return MrConvert(name=name, out_file="out" + out_ext, **kwargs)


# @converter(
#     source_format=MedicalImage,
#     target_format=MrtrixImageHeader,
#     out_ext=MrtrixImageHeader.ext,
#     **in_out_file_kwargs,
# )
# def mrconvert2(name, out_ext: str, **kwargs):
#     """Initiate an MRConvert task with the output file extension set

#     Parameters
#     ----------
#     name : str
#         name of the converter task
#     out_ext : str
#         extension of the output file, used by MRConvert to determine the desired format

#     Returns
#     -------
#     pydra.ShellCommandTask
#         the converter task
#     """
#     return MrConvert(name=name, out_file="out" + out_ext, **kwargs)
