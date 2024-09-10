# Auto-generated test for dwi2mask_ants

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Mask_Ants


@pytest.mark.xfail(reason="Task dwi2mask_ants is known not pass yet")
def test_dwi2mask_ants(tmp_path, cli_parse_only):

    task = Dwi2Mask_Ants(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        template=Nifti1.sample(),
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
