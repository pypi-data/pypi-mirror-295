# Auto-generated test for dwi2mask_trace

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Mask_Trace


@pytest.mark.xfail(reason="Task dwi2mask_trace is known not pass yet")
def test_dwi2mask_trace(tmp_path, cli_parse_only):

    task = Dwi2Mask_Trace(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        iterative=True,
        max_iters=1,
        shells=list([1.0]),
        clean_scale=1,
        grad=File.sample(),
        fslgrad=File.sample(),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
