# Auto-generated test for dwifslpreproc

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiFslpreproc


@pytest.mark.xfail(reason="Task dwifslpreproc is known not pass yet")
def test_dwifslpreproc(tmp_path, cli_parse_only):

    task = DwiFslpreproc(
        in_file=Nifti1.sample(),
        out_file=ImageFormat.sample(),
        rpe_none=True,
        rpe_pair=True,
        rpe_all=True,
        rpe_header=True,
        grad=File.sample(),
        fslgrad=File.sample(),
        export_grad_mrtrix=False,
        export_grad_fsl=False,
        eddyqc_text=False,
        eddyqc_all=False,
        eddy_mask=Nifti1.sample(),
        eddy_slspec=File.sample(),
        eddy_options="a-string",
        se_epi=Nifti1.sample(),
        align_seepi=True,
        topup_options="a-string",
        topup_files="a-string",
        pe_dir="a-string",
        readout_time=1.0,
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
        json_import=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
