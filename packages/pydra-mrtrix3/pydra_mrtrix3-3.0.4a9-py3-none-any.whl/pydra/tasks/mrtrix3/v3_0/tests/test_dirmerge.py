# Auto-generated test for dirmerge

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DirMerge


def test_dirmerge(tmp_path, cli_parse_only):

    task = DirMerge(
        subsets=1,
        bvalue_files=["a-string"],
        out=File.sample(),
        unipolar_weight=1.0,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
