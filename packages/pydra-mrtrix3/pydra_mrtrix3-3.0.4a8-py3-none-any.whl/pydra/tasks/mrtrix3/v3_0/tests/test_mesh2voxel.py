# Auto-generated test for mesh2voxel

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Mesh2Voxel


def test_mesh2voxel(tmp_path, cli_parse_only):

    task = Mesh2Voxel(
        source=File.sample(),
        template=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
