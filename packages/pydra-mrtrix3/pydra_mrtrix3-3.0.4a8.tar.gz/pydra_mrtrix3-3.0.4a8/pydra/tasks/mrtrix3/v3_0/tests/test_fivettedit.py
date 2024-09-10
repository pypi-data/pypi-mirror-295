# Auto-generated test for fivettedit

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FivettEdit


def test_fivettedit(tmp_path, cli_parse_only):

    task = FivettEdit(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        cgm=Nifti1.sample(),
        sgm=Nifti1.sample(),
        wm=Nifti1.sample(),
        csf=Nifti1.sample(),
        path=Nifti1.sample(),
        none=Nifti1.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
