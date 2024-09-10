# Auto-generated test for meshconvert

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MeshConvert


def test_meshconvert(tmp_path, cli_parse_only):

    task = MeshConvert(
        in_file=File.sample(),
        out_file=File.sample(),
        binary=True,
        transform=tuple(["a-string", "a-string"]),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
