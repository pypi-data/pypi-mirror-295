# Auto-generated test for dirsplit

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DirSplit


@pytest.mark.xfail(reason="Task dirsplit is known not pass yet")
def test_dirsplit(tmp_path, cli_parse_only):

    task = DirSplit(
        dirs=File.sample(),
        out=File.sample(),
        permutations=1,
        cartesian=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
