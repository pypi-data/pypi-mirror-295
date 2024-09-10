# Auto-generated test for mrmath

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrMath


def test_mrmath(tmp_path, cli_parse_only):

    task = MrMath(
        in_file=[Nifti1.sample()],
        operation="mean",
        out_file=ImageFormat.sample(),
        axis=1,
        keep_unary_axes=True,
        datatype="float16",
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
