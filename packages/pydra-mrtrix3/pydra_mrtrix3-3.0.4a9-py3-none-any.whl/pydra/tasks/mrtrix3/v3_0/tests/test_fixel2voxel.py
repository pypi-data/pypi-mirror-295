# Auto-generated test for fixel2voxel

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Fixel2Voxel


def test_fixel2voxel(tmp_path, cli_parse_only):

    task = Fixel2Voxel(
        fixel_in=Nifti1.sample(),
        operation="mean",
        image_out=ImageFormat.sample(),
        number=1,
        fill=1.0,
        weighted=Nifti1.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
