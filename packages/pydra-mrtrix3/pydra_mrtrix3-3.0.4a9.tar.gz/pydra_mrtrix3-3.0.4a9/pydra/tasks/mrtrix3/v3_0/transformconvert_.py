# Auto-generated from MRtrix C++ command with '__print_usage_pydra__' secret option

import typing as ty
from pathlib import Path  # noqa: F401
from fileformats.generic import File, Directory  # noqa: F401
from fileformats.medimage_mrtrix3 import ImageIn, ImageOut, Tracks  # noqa: F401
from pydra.engine import specs, ShellCommandTask


input_fields = [
    # Arguments
    (
        "input",
        specs.MultiInputObj[ty.Any],
        {
            "argstr": "",
            "position": 0,
            "help_string": """the input(s) for the specified operation""",
            "mandatory": True,
        },
    ),
    (
        "operation",
        str,
        {
            "argstr": "",
            "position": 1,
            "help_string": """the operation to perform, one of:
flirt_import, itk_import""",
            "mandatory": True,
            "allowed_values": ["flirt_import", "flirt_import", "itk_import"],
        },
    ),
    (
        "out_file",
        Path,
        {
            "argstr": "",
            "position": 2,
            "output_file_template": "out_file.txt",
            "help_string": """the output transformation matrix.""",
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

TransformConvertInputSpec = specs.SpecInfo(
    name="TransformConvertInput", fields=input_fields, bases=(specs.ShellSpec,)
)


output_fields = [
    (
        "out_file",
        File,
        {
            "help_string": """the output transformation matrix.""",
        },
    ),
]
TransformConvertOutputSpec = specs.SpecInfo(
    name="TransformConvertOutput", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class TransformConvert(ShellCommandTask):
    """This command allows to convert transformation matrices provided by other registration softwares to a format usable in MRtrix3. Example usages are provided below.


        Example usages
        --------------


        Convert a transformation matrix produced by FSL's flirt command into a format usable by MRtrix3:

            `$ transformconvert transform_flirt.mat flirt_in.nii flirt_ref.nii flirt_import transform_mrtrix.txt`

            The two images provided as inputs for this operation must be in the correct order: first the image that was provided to flirt via the -in option, second the image that was provided to flirt via the -ref option.


        Convert a plain text transformation matrix file produced by ITK's affine registration (e.g. ANTS, Slicer) into a format usable by MRtrix3:

            `$ transformconvert transform_itk.txt itk_import transform_mrtrix.txt`



        References
        ----------

            Tournier, J.-D.; Smith, R. E.; Raffelt, D.; Tabbara, R.; Dhollander, T.; Pietsch, M.; Christiaens, D.; Jeurissen, B.; Yeh, C.-H. & Connelly, A. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. NeuroImage, 2019, 202, 116137


        MRtrix
        ------

            Version:3.0.4, built Sep 10 2024

            Author: Max Pietsch (maximilian.pietsch@kcl.ac.uk)

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

    executable = "transformconvert"
    input_spec = TransformConvertInputSpec
    output_spec = TransformConvertOutputSpec
