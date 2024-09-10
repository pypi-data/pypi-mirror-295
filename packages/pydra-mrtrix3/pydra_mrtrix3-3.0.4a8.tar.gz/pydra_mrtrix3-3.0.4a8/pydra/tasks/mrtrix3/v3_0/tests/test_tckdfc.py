# Auto-generated test for tckdfc

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import TckDfc


def test_tckdfc(tmp_path, cli_parse_only):

    task = TckDfc(
        tracks=File.sample(),
        fmri=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        static=True,
        dynamic=tuple(["a-string", "a-string"]),
        template=Nifti1.sample(),
        vox=list([1.0]),
        stat_vox="sum",
        backtrack=True,
        upsample=1,
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
