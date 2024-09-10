# Auto-generated test for dwi2mask_consensus

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Mask_Consensus


@pytest.mark.xfail(reason="Task dwi2mask_consensus is known not pass yet")
def test_dwi2mask_consensus(tmp_path, cli_parse_only):

    task = Dwi2Mask_Consensus(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        algorithms="a-string",
        masks=False,
        template=Nifti1.sample(),
        threshold=1.0,
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
