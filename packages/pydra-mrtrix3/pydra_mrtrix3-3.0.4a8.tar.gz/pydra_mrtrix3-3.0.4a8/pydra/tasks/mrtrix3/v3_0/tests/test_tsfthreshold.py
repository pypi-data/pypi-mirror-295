# Auto-generated test for tsfthreshold

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import TsfThreshold


def test_tsfthreshold(tmp_path, cli_parse_only):

    task = TsfThreshold(
        in_file=File.sample(),
        T=1.0,
        out_file=File.sample(),
        invert=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
