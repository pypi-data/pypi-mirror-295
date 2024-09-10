# Auto-generated test for dwi2mask_b02template

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Mask_B02template


@pytest.mark.xfail(reason="Task dwi2mask_b02template is known not pass yet")
def test_dwi2mask_b02template(tmp_path, cli_parse_only):

    task = Dwi2Mask_B02template(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        flirt_options="a-string",
        fnirt_config=File.sample(),
        ants_options="a-string",
        software="antsfull",
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
