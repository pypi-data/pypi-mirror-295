# Auto-generated test for mrregister

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrRegister


def test_mrregister(tmp_path, cli_parse_only):

    task = MrRegister(
        image1_image2=Nifti1.sample(),
        contrast1_contrast2=[Nifti1.sample()],
        type="rigid",
        transformed=[ImageFormat.sample()],
        transformed_midway=[tuple([ImageFormat.sample(), ImageFormat.sample()])],
        mask1=Nifti1.sample(),
        mask2=Nifti1.sample(),
        nan=True,
        rigid=False,
        rigid_1tomidway=False,
        rigid_2tomidway=False,
        rigid_init_translation="mass",
        rigid_init_rotation="search",
        rigid_init_matrix=File.sample(),
        rigid_scale=list([1.0]),
        rigid_niter=list([1]),
        rigid_metric="diff",
        rigid_metric_diff_estimator="l1",
        rigid_lmax=list([1]),
        rigid_log=False,
        affine=False,
        affine_1tomidway=False,
        affine_2tomidway=False,
        affine_init_translation="mass",
        affine_init_rotation="search",
        affine_init_matrix=File.sample(),
        affine_scale=list([1.0]),
        affine_niter=list([1]),
        affine_metric="diff",
        affine_metric_diff_estimator="l1",
        affine_lmax=list([1]),
        affine_log=False,
        init_translation_unmasked1=True,
        init_translation_unmasked2=True,
        init_rotation_unmasked1=True,
        init_rotation_unmasked2=True,
        init_rotation_search_angles=list([1.0]),
        init_rotation_search_scale=1.0,
        init_rotation_search_directions=1,
        init_rotation_search_run_global=True,
        init_rotation_search_global_iterations=1,
        linstage_iterations=list([1]),
        linstage_optimiser_first="bbgd",
        linstage_optimiser_last="bbgd",
        linstage_optimiser_default="bbgd",
        linstage_diagnostics_prefix="a-string",
        nl_warp=False,
        nl_warp_full=False,
        nl_init=Nifti1.sample(),
        nl_scale=list([1.0]),
        nl_niter=list([1]),
        nl_update_smooth=1.0,
        nl_disp_smooth=1.0,
        nl_grad_step=1.0,
        nl_lmax=list([1]),
        diagnostics_image=File.sample(),
        directions=File.sample(),
        noreorientation=True,
        mc_weights=list([1.0]),
        datatype="float16",
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
