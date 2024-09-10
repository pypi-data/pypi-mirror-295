# Auto-generated test for sh2peaks

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Sh2Peaks


def test_sh2peaks(tmp_path, cli_parse_only):

    task = Sh2Peaks(
        SH=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        num=1,
        direction=[tuple([1.0, 1.0])],
        peaks=Nifti1.sample(),
        threshold=1.0,
        seeds=File.sample(),
        mask=Nifti1.sample(),
        fast=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
