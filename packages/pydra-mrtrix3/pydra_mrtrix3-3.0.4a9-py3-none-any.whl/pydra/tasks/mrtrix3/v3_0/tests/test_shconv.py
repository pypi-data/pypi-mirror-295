# Auto-generated test for shconv

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import ShConv


def test_shconv(tmp_path, cli_parse_only):

    task = ShConv(
        odf_response=[File.sample()],
        SH_out=ImageFormat.sample(),
        datatype="float16",
        strides=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
