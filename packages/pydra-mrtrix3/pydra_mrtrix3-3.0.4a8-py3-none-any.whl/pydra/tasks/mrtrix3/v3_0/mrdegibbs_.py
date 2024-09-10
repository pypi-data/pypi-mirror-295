# Auto-generated from MRtrix C++ command with '__print_usage_pydra__' secret option

import typing as ty
from pathlib import Path  # noqa: F401
from fileformats.generic import File, Directory  # noqa: F401
from fileformats.medimage_mrtrix3 import ImageIn, ImageOut, Tracks  # noqa: F401
from pydra.engine import specs, ShellCommandTask


input_fields = [
    # Arguments
    (
        "in_",
        ImageIn,
        {
            "argstr": "",
            "position": 0,
            "help_string": """the input image.""",
            "mandatory": True,
        },
    ),
    (
        "out",
        Path,
        {
            "argstr": "",
            "position": 1,
            "output_file_template": "out.mif",
            "help_string": """the output image.""",
        },
    ),
    (
        "mode",
        str,
        {
            "argstr": "-mode",
            "help_string": """specify the mode of operation. Valid choices are: 2d, 3d (default: 2d). The 2d mode corresponds to the original slice-wise approach as propoosed by Kellner et al., appropriate for images acquired using 2D muli-slice approaches. The 3d mode corresponds to the 3D volume-wise extension proposed by Bautista et al., which is appropriate for images acquired using 3D Fourier encoding.""",
            "allowed_values": ["2d", "2d", "3d"],
        },
    ),
    (
        "axes",
        ty.List[int],
        {
            "argstr": "-axes",
            "help_string": """select the slice axes (default: 0,1 - i.e. x-y). Select all 3 spatial axes for 3D operation, i.e. 0:2 or 0,1,2 (this is equivalent to '-mode 3d').""",
            "sep": ",",
        },
    ),
    (
        "nshifts",
        int,
        {
            "argstr": "-nshifts",
            "help_string": """discretization of subpixel spacing (default: 20).""",
        },
    ),
    (
        "minW",
        int,
        {
            "argstr": "-minW",
            "help_string": """left border of window used for TV computation (default: 1).""",
        },
    ),
    (
        "maxW",
        int,
        {
            "argstr": "-maxW",
            "help_string": """right border of window used for TV computation (default: 3).""",
        },
    ),
    # Data type options Option Group
    (
        "datatype",
        str,
        {
            "argstr": "-datatype",
            "help_string": """specify output image data type. Valid choices are: float16, float16le, float16be, float32, float32le, float32be, float64, float64le, float64be, int64, uint64, int64le, uint64le, int64be, uint64be, int32, uint32, int32le, uint32le, int32be, uint32be, int16, uint16, int16le, uint16le, int16be, uint16be, cfloat16, cfloat16le, cfloat16be, cfloat32, cfloat32le, cfloat32be, cfloat64, cfloat64le, cfloat64be, int8, uint8, bit.""",
            "allowed_values": [
                "float16",
                "float16",
                "float16le",
                "float16be",
                "float32",
                "float32le",
                "float32be",
                "float64",
                "float64le",
                "float64be",
                "int64",
                "uint64",
                "int64le",
                "uint64le",
                "int64be",
                "uint64be",
                "int32",
                "uint32",
                "int32le",
                "uint32le",
                "int32be",
                "uint32be",
                "int16",
                "uint16",
                "int16le",
                "uint16le",
                "int16be",
                "uint16be",
                "cfloat16",
                "cfloat16le",
                "cfloat16be",
                "cfloat32",
                "cfloat32le",
                "cfloat32be",
                "cfloat64",
                "cfloat64le",
                "cfloat64be",
                "int8",
                "uint8",
                "bit",
            ],
        },
    ),
    # Standard options
    (
        "info",
        bool,
        {
            "argstr": "-info",
            "help_string": """display information messages.""",
        },
    ),
    (
        "quiet",
        bool,
        {
            "argstr": "-quiet",
            "help_string": """do not display information messages or progress status; alternatively, this can be achieved by setting the MRTRIX_QUIET environment variable to a non-empty string.""",
        },
    ),
    (
        "debug",
        bool,
        {
            "argstr": "-debug",
            "help_string": """display debugging messages.""",
        },
    ),
    (
        "force",
        bool,
        {
            "argstr": "-force",
            "help_string": """force overwrite of output files (caution: using the same file as input and output might cause unexpected behaviour).""",
        },
    ),
    (
        "nthreads",
        int,
        {
            "argstr": "-nthreads",
            "help_string": """use this number of threads in multi-threaded applications (set to 0 to disable multi-threading).""",
        },
    ),
    (
        "config",
        specs.MultiInputObj[ty.Tuple[str, str]],
        {
            "argstr": "-config",
            "help_string": """temporarily set the value of an MRtrix config file entry.""",
        },
    ),
    (
        "help",
        bool,
        {
            "argstr": "-help",
            "help_string": """display this information page and exit.""",
        },
    ),
    (
        "version",
        bool,
        {
            "argstr": "-version",
            "help_string": """display version information and exit.""",
        },
    ),
]

MrDegibbsInputSpec = specs.SpecInfo(
    name="MrDegibbsInput", fields=input_fields, bases=(specs.ShellSpec,)
)


output_fields = [
    (
        "out",
        ImageOut,
        {
            "help_string": """the output image.""",
        },
    ),
]
MrDegibbsOutputSpec = specs.SpecInfo(
    name="MrDegibbsOutput", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class MrDegibbs(ShellCommandTask):
    """This application attempts to remove Gibbs ringing artefacts from MRI images using the method of local subvoxel-shifts proposed by Kellner et al. (see reference below for details). By default, the original 2D slice-wise version is used. If the -mode 3d option is provided, the program will run the 3D version as proposed by Bautista et al. (also in the reference list below).

        This command is designed to run on data directly after it has been reconstructed by the scanner, before any interpolation of any kind has taken place. You should not run this command after any form of motion correction (e.g. not after dwifslpreproc). Similarly, if you intend running dwidenoise, you should run denoising before this command to not alter the noise structure, which would impact on dwidenoise's performance.

        Note that this method is designed to work on images acquired with full k-space coverage. Running this method on partial Fourier ('half-scan') or filtered data may not remove all ringing artefacts. Users are encouraged to acquired full-Fourier data where possible, and disable any form of filtering on the scanner.


        References
        ----------

            Kellner, E; Dhital, B; Kiselev, V.G & Reisert, M. Gibbs-ringing artifact removal based on local subvoxel-shifts. Magnetic Resonance in Medicine, 2016, 76, 1574–1581.

            Bautista, T; O’Muircheartaigh, J; Hajnal, JV; & Tournier, J-D. Removal of Gibbs ringing artefacts for 3D acquisitions using subvoxel shifts. Proc. ISMRM, 2021, 29, 3535.

            Tournier, J.-D.; Smith, R. E.; Raffelt, D.; Tabbara, R.; Dhollander, T.; Pietsch, M.; Christiaens, D.; Jeurissen, B.; Yeh, C.-H. & Connelly, A. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. NeuroImage, 2019, 202, 116137


        MRtrix
        ------

            Version:3.0.4, built Sep 10 2024

            Author: Ben Jeurissen (ben.jeurissen@uantwerpen.be) & J-Donald Tournier (jdtournier@gmail.com)

            Copyright: Copyright (c) 2008-2024 the MRtrix3 contributors.

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.

    Covered Software is provided under this License on an "as is"
    basis, without warranty of any kind, either expressed, implied, or
    statutory, including, without limitation, warranties that the
    Covered Software is free of defects, merchantable, fit for a
    particular purpose or non-infringing.
    See the Mozilla Public License v. 2.0 for more details.

    For more details, see http://www.mrtrix.org/.
    """

    executable = "mrdegibbs"
    input_spec = MrDegibbsInputSpec
    output_spec = MrDegibbsOutputSpec
