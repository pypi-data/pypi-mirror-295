# Auto-generated test for fod2dec

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Fod2Dec


def test_fod2dec(tmp_path, cli_parse_only):

    task = Fod2Dec(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        mask=Nifti1.sample(),
        contrast=Nifti1.sample(),
        lum=True,
        lum_coefs=list([1.0]),
        lum_gamma=1.0,
        threshold=1.0,
        no_weight=True,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
