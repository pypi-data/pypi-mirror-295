# Auto-generated test for fixelconvert

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FixelConvert


@pytest.mark.xfail(reason="Task fixelconvert is known not pass yet")
def test_fixelconvert(tmp_path, cli_parse_only):

    task = FixelConvert(
        fixel_in=File.sample(),
        fixel_out=File.sample(),
        name="a-string",
        nii=True,
        out_size=True,
        template=File.sample(),
        value=File.sample(),
        in_size=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
