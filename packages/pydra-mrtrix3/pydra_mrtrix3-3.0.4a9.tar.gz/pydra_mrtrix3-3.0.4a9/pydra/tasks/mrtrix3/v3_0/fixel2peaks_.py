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
        ty.Any,
        {
            "argstr": "",
            "position": 0,
            "help_string": """the input fixel information""",
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
            "help_string": """the output peaks image""",
        },
    ),
    (
        "number",
        int,
        {
            "argstr": "-number",
            "help_string": """maximum number of fixels in each voxel (default: based on input data)""",
        },
    ),
    (
        "nan",
        bool,
        {
            "argstr": "-nan",
            "help_string": """fill excess peak data with NaNs rather than zeroes""",
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

Fixel2PeaksInputSpec = specs.SpecInfo(
    name="Fixel2PeaksInput", fields=input_fields, bases=(specs.ShellSpec,)
)


output_fields = [
    (
        "out",
        ImageOut,
        {
            "help_string": """the output peaks image""",
        },
    ),
]
Fixel2PeaksOutputSpec = specs.SpecInfo(
    name="Fixel2PeaksOutput", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class Fixel2Peaks(ShellCommandTask):
    """If a fixel data file is provided as input, then the 3-vectors in the output image will be scaled based on the data in that file. If the input is instead the fixel directory, or the index or directions file, then all output 3-vectors will possess unit norm.

        Fixel data are stored utilising the fixel directory format described in the main documentation, which can be found at the following link:
    https://mrtrix.readthedocs.io/en/3.0.4/fixel_based_analysis/fixel_directory_format.html


        References
        ----------

            Tournier, J.-D.; Smith, R. E.; Raffelt, D.; Tabbara, R.; Dhollander, T.; Pietsch, M.; Christiaens, D.; Jeurissen, B.; Yeh, C.-H. & Connelly, A. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. NeuroImage, 2019, 202, 116137


        MRtrix
        ------

            Version:3.0.4, built Sep 10 2024

            Author: Robert E. Smith (robert.smith@florey.edu.au)

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

    executable = "fixel2peaks"
    input_spec = Fixel2PeaksInputSpec
    output_spec = Fixel2PeaksOutputSpec
