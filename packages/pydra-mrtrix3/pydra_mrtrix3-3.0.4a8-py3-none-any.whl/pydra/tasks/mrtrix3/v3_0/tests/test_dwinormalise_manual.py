# Auto-generated test for dwinormalise_manual

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiNormalise_Manual


@pytest.mark.xfail(reason="Task dwinormalise_manual is known not pass yet")
def test_dwinormalise_manual(tmp_path, cli_parse_only):

    task = DwiNormalise_Manual(
        input_dwi=Nifti1.sample(),
        input_mask=Nifti1.sample(),
        output_dwi=ImageFormat.sample(),
        grad=File.sample(),
        fslgrad=File.sample(),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        intensity=1.0,
        percentile=1.0,
    )
    result = task(plugin="serial")
    assert not result.errored
