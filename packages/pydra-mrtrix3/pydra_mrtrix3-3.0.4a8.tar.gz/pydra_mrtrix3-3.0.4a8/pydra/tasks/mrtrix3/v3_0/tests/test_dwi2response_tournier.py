# Auto-generated test for dwi2response_tournier

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Response_Tournier


@pytest.mark.xfail(reason="Task dwi2response_tournier is known not pass yet")
def test_dwi2response_tournier(tmp_path, cli_parse_only):

    task = Dwi2Response_Tournier(
        in_file=Nifti1.sample(),
        out_file=File.sample(),
        number=1,
        iter_voxels=1,
        dilate=1,
        max_iters=1,
        grad=File.sample(),
        fslgrad=File.sample(),
        mask=Nifti1.sample(),
        voxels=False,
        shells=list([1.0]),
        lmax=list([1]),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
