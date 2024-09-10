# Auto-generated test for labelsgmfix

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import LabelSgmfix


@pytest.mark.xfail(reason="Task labelsgmfix is known not pass yet")
def test_labelsgmfix(tmp_path, cli_parse_only):

    task = LabelSgmfix(
        parc=Nifti1.sample(),
        t1=Nifti1.sample(),
        lut=File.sample(),
        out_file=ImageFormat.sample(),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        premasked=True,
        sgm_amyg_hipp=True,
    )
    result = task(plugin="serial")
    assert not result.errored
