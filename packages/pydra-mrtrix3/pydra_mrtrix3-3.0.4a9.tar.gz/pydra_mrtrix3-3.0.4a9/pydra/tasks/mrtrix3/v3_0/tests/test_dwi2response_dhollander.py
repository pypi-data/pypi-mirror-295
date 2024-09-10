# Auto-generated test for dwi2response_dhollander

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Response_Dhollander


@pytest.mark.xfail(reason="Task dwi2response_dhollander is known not pass yet")
def test_dwi2response_dhollander(tmp_path, cli_parse_only):

    task = Dwi2Response_Dhollander(
        in_file=Nifti1.sample(),
        out_sfwm=File.sample(),
        out_gm=File.sample(),
        out_csf=File.sample(),
        erode=1,
        fa=1.0,
        sfwm=1.0,
        gm=1.0,
        csf=1.0,
        wm_algo="fa",
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
