# Auto-generated test for mask2glass

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Mask2Glass


@pytest.mark.xfail(reason="Task mask2glass is known not pass yet")
def test_mask2glass(tmp_path, cli_parse_only):

    task = Mask2Glass(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        dilate=1,
        scale=1.0,
        smooth=1.0,
    )
    result = task(plugin="serial")
    assert not result.errored
