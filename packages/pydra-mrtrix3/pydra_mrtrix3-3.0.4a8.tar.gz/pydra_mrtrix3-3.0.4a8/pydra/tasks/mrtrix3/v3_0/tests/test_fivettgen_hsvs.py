# Auto-generated test for fivettgen_hsvs

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FivettGen_Hsvs


@pytest.mark.xfail(reason="Task fivettgen_hsvs is known not pass yet")
def test_fivettgen_hsvs(tmp_path, cli_parse_only):

    task = FivettGen_Hsvs(
        in_file=File.sample(),
        out_file=ImageFormat.sample(),
        nocrop=True,
        sgm_amyg_hipp=True,
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        template=Nifti1.sample(),
        hippocampi="subfields",
        thalami="nuclei",
        white_stem=True,
    )
    result = task(plugin="serial")
    assert not result.errored
