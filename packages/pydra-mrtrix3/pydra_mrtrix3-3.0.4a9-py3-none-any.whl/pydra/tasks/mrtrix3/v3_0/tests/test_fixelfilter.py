# Auto-generated test for fixelfilter

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FixelFilter


@pytest.mark.xfail(reason="Task fixelfilter is known not pass yet")
def test_fixelfilter(tmp_path, cli_parse_only):

    task = FixelFilter(
        input=File.sample(),
        filter="connect",
        output=File.sample(),
        matrix=File.sample(),
        threshold_value=1.0,
        threshold_connectivity=1.0,
        fwhm=1.0,
        minweight=1.0,
        mask=Nifti1.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
