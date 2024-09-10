# Auto-generated test for fivettgen_gif

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FivettGen_Gif


@pytest.mark.xfail(reason="Task fivettgen_gif is known not pass yet")
def test_fivettgen_gif(tmp_path, cli_parse_only):

    task = FivettGen_Gif(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        nocrop=True,
        sgm_amyg_hipp=True,
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
