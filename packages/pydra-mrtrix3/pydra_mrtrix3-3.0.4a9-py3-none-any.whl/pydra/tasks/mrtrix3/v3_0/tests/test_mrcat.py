# Auto-generated test for mrcat

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrCat


def test_mrcat(tmp_path, cli_parse_only):

    task = MrCat(
        image1=Nifti1.sample(),
        image2=[Nifti1.sample()],
        out_file=ImageFormat.sample(),
        axis=1,
        datatype="float16",
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
