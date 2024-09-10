# Auto-generated test for dwibiasnormmask

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiBiasnormmask


@pytest.mark.xfail(reason="Task dwibiasnormmask is known not pass yet")
def test_dwibiasnormmask(tmp_path, cli_parse_only):

    task = DwiBiasnormmask(
        in_file=Nifti1.sample(),
        output_dwi=ImageFormat.sample(),
        output_mask=ImageFormat.sample(),
        grad=File.sample(),
        fslgrad=File.sample(),
        dice=1.0,
        init_mask=Nifti1.sample(),
        max_iters=1,
        mask_algo="dwi2mask",
        lmax=list([1]),
        output_bias=False,
        output_scale=False,
        output_tissuesum=False,
        reference=1.0,
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
