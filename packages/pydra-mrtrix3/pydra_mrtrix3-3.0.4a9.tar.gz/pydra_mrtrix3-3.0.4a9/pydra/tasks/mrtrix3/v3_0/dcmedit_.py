# Auto-generated from MRtrix C++ command with '__print_usage_pydra__' secret option

import typing as ty
from pathlib import Path  # noqa: F401
from fileformats.generic import File, Directory  # noqa: F401
from fileformats.medimage_mrtrix3 import ImageIn, ImageOut, Tracks  # noqa: F401
from pydra.engine import specs, ShellCommandTask


input_fields = [
    # Arguments
    (
        "file",
        File,
        {
            "argstr": "",
            "position": 0,
            "help_string": """the DICOM file to be edited.""",
            "mandatory": True,
        },
    ),
    (
        "anonymise",
        bool,
        {
            "argstr": "-anonymise",
            "help_string": """remove any identifiable information, by replacing the following tags:
- any tag with Value Representation PN will be replaced with 'anonymous'
- tag (0010,0030) PatientBirthDate will be replaced with an empty string
WARNING: there is no guarantee that this command will remove all identiable information, since such information may be contained in any number of private vendor-specific tags. You will need to double-check the results independently if you need to ensure anonymity.""",
        },
    ),
    (
        "id",
        str,
        {
            "argstr": "-id",
            "help_string": """replace all ID tags with string supplied. This consists of tags (0010, 0020) PatientID and (0010, 1000) OtherPatientIDs""",
        },
    ),
    (
        "tag",
        specs.MultiInputObj[ty.Tuple[ty.Any, ty.Any, ty.Any]],
        {
            "argstr": "-tag",
            "help_string": """replace specific tag.""",
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

DcmEditInputSpec = specs.SpecInfo(
    name="DcmEditInput", fields=input_fields, bases=(specs.ShellSpec,)
)


output_fields = []
DcmEditOutputSpec = specs.SpecInfo(
    name="DcmEditOutput", fields=output_fields, bases=(specs.ShellOutSpec,)
)


class DcmEdit(ShellCommandTask):
    """Note that this command simply replaces the existing values without modifying the DICOM structure in any way. Replacement text will be truncated if it is too long to fit inside the existing tag.

        WARNING: this command will modify existing data! It is recommended to run this command on a copy of the original data set to avoid loss of data.


        References
        ----------

            Tournier, J.-D.; Smith, R. E.; Raffelt, D.; Tabbara, R.; Dhollander, T.; Pietsch, M.; Christiaens, D.; Jeurissen, B.; Yeh, C.-H. & Connelly, A. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. NeuroImage, 2019, 202, 116137


        MRtrix
        ------

            Version:3.0.4, built Sep 10 2024

            Author: J-Donald Tournier (jdtournier@gmail.com)

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

    executable = "dcmedit"
    input_spec = DcmEditInputSpec
    output_spec = DcmEditOutputSpec
