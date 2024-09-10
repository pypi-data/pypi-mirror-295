# Auto-generated test for amp2response

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Amp2Response


def test_amp2response(tmp_path, cli_parse_only):

    task = Amp2Response(
        amps=Nifti1.sample(),
        mask=Nifti1.sample(),
        directions_image=Nifti1.sample(),
        response=File.sample(),
        isotropic=True,
        noconstraint=True,
        directions=File.sample(),
        shells=list([1.0]),
        lmax=list([1]),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
