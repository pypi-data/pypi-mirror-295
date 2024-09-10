# Auto-generated test for peaks2fixel

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Peaks2Fixel


def test_peaks2fixel(tmp_path, cli_parse_only):

    task = Peaks2Fixel(
        directions=Nifti1.sample(),
        fixels=Directory.sample(),
        dataname="a-string",
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
