# Auto-generated test for warpinvert

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import WarpInvert


@pytest.mark.xfail(reason="Task warpinvert is known not pass yet")
def test_warpinvert(tmp_path, cli_parse_only):

    task = WarpInvert(
        in_=Nifti1.sample(),
        out=ImageFormat.sample(),
        template=Nifti1.sample(),
        displacement=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
