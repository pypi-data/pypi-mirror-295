# Auto-generated test for dwigradcheck

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiGradcheck


@pytest.mark.xfail(reason="Task dwigradcheck is known not pass yet")
def test_dwigradcheck(tmp_path, cli_parse_only):

    task = DwiGradcheck(
        in_file=Nifti1.sample(),
        grad=File.sample(),
        fslgrad=File.sample(),
        export_grad_mrtrix=False,
        export_grad_fsl=False,
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        mask=Nifti1.sample(),
        number=1,
    )
    result = task(plugin="serial")
    assert not result.errored
