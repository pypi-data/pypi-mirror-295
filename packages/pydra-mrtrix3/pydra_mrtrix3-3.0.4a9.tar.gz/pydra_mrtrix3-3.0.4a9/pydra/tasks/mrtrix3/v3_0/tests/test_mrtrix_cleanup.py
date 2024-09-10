# Auto-generated test for mrtrix_cleanup

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrTrix_Cleanup


@pytest.mark.xfail(reason="Task mrtrix_cleanup is known not pass yet")
def test_mrtrix_cleanup(tmp_path, cli_parse_only):

    task = MrTrix_Cleanup(
        path=File.sample(),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        test=True,
        failed=False,
    )
    result = task(plugin="serial")
    assert not result.errored
