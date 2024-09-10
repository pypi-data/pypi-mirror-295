# Auto-generated test for voxel2mesh

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Voxel2Mesh


def test_voxel2mesh(tmp_path, cli_parse_only):

    task = Voxel2Mesh(
        in_file=Nifti1.sample(),
        out_file=File.sample(),
        blocky=True,
        threshold=1.0,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
