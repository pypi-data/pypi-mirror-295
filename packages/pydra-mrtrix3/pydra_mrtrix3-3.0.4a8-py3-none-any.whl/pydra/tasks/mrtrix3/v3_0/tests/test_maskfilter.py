# Auto-generated test for maskfilter

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MaskFilter


def test_maskfilter(tmp_path, cli_parse_only):

    task = MaskFilter(
        in_file=Nifti1.sample(),
        filter="clean",
        out_file=ImageFormat.sample(),
        scale=1,
        axes=list([1]),
        largest=True,
        connectivity=True,
        minsize=1,
        npass=1,
        extent=list([1]),
        strides=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
