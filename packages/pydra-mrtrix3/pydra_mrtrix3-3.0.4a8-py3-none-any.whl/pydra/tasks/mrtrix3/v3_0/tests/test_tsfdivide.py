# Auto-generated test for tsfdivide

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import TsfDivide


def test_tsfdivide(tmp_path, cli_parse_only):

    task = TsfDivide(
        input1=File.sample(),
        input2=File.sample(),
        out_file=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
