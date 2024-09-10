# Auto-generated test for sh2response

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Sh2Response


def test_sh2response(tmp_path, cli_parse_only):

    task = Sh2Response(
        SH=Nifti1.sample(),
        mask=Nifti1.sample(),
        directions=Nifti1.sample(),
        response=File.sample(),
        lmax=1,
        dump=False,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
