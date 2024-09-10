# Auto-generated test for mrcheckerboardmask

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrCheckerboardmask


def test_mrcheckerboardmask(tmp_path, cli_parse_only):

    task = MrCheckerboardmask(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        tiles=1,
        invert=True,
        nan=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
