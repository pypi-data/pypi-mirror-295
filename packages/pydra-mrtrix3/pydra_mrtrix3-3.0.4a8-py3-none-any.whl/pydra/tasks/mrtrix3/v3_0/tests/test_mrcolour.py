# Auto-generated test for mrcolour

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrColour


def test_mrcolour(tmp_path, cli_parse_only):

    task = MrColour(
        in_file=Nifti1.sample(),
        map="gray",
        out_file=ImageFormat.sample(),
        upper=1.0,
        lower=1.0,
        colour=list([1.0]),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
