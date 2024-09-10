# Auto-generated test for tckinfo

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import TckInfo


def test_tckinfo(tmp_path, cli_parse_only):

    task = TckInfo(
        tracks=[Tracks.sample()],
        count=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
