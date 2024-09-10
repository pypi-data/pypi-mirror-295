# Auto-generated test for fivett2vis

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Fivett2Vis


def test_fivett2vis(tmp_path, cli_parse_only):

    task = Fivett2Vis(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        bg=1.0,
        cgm=1.0,
        sgm=1.0,
        wm=1.0,
        csf=1.0,
        path=1.0,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
