# Auto-generated test for dwinormalise_mtnorm

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiNormalise_Mtnorm


@pytest.mark.xfail(reason="Task dwinormalise_mtnorm is known not pass yet")
def test_dwinormalise_mtnorm(tmp_path, cli_parse_only):

    task = DwiNormalise_Mtnorm(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        grad=File.sample(),
        fslgrad=File.sample(),
        lmax=list([1]),
        mask=Nifti1.sample(),
        reference=1.0,
        scale=False,
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
