# Auto-generated test for dwi2mask_3dautomask

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Mask_3dautomask


@pytest.mark.xfail(reason="Task dwi2mask_3dautomask is known not pass yet")
def test_dwi2mask_3dautomask(tmp_path, cli_parse_only):

    task = Dwi2Mask_3dautomask(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        clfrac=1.0,
        nograd=True,
        peels=1,
        nbhrs=1,
        eclip=True,
        SI=1.0,
        dilate=1,
        erode=1,
        NN1=True,
        NN2=True,
        NN3=True,
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
