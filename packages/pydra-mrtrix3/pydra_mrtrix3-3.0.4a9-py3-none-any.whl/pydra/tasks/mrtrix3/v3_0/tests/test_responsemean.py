# Auto-generated test for responsemean

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import ResponseMean


@pytest.mark.xfail(reason="Task responsemean is known not pass yet")
def test_responsemean(tmp_path, cli_parse_only):

    task = ResponseMean(
        inputs=File.sample(),
        out_file=File.sample(),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        legacy=True,
    )
    result = task(plugin="serial")
    assert not result.errored
