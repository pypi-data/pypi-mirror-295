# Auto-generated test for mrhistogram

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrHistogram


def test_mrhistogram(tmp_path, cli_parse_only):

    task = MrHistogram(
        image_=Nifti1.sample(),
        hist=File.sample(),
        bins=1,
        template=File.sample(),
        mask=Nifti1.sample(),
        ignorezero=True,
        allvolumes=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
