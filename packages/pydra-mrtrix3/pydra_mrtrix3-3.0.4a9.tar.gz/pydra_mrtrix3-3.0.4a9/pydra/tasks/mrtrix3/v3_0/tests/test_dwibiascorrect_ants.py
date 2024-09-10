# Auto-generated test for dwibiascorrect_ants

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiBiascorrect_Ants


@pytest.mark.xfail(reason="Task dwibiascorrect_ants is known not pass yet")
def test_dwibiascorrect_ants(tmp_path, cli_parse_only):

    task = DwiBiascorrect_Ants(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        ants_b="a-string",
        ants_c="a-string",
        ants_s="a-string",
        grad=File.sample(),
        fslgrad=File.sample(),
        mask=Nifti1.sample(),
        bias=False,
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
