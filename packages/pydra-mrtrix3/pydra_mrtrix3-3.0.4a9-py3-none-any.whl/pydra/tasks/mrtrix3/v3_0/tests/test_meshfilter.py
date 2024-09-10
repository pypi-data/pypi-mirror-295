# Auto-generated test for meshfilter

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MeshFilter


def test_meshfilter(tmp_path, cli_parse_only):

    task = MeshFilter(
        in_file=File.sample(),
        filter="smooth",
        out_file=File.sample(),
        smooth_spatial=1.0,
        smooth_influence=1.0,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
