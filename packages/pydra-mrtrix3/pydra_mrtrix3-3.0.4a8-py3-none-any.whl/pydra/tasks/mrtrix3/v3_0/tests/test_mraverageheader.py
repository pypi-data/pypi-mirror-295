# Auto-generated test for mraverageheader

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrAverageheader


def test_mraverageheader(tmp_path, cli_parse_only):

    task = MrAverageheader(
        in_file=[Nifti1.sample()],
        out_file=ImageFormat.sample(),
        padding=1.0,
        resolution="max",
        fill=True,
        datatype="float16",
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
