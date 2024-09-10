# Auto-generated test for population_template

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import PopulationTemplate


@pytest.mark.xfail(reason="Task population_template is known not pass yet")
def test_population_template(tmp_path, cli_parse_only):

    task = PopulationTemplate(
        input_dir=File.sample(),
        template=ImageFormat.sample(),
        type="rigid",
        voxel_size=list([1.0]),
        initial_alignment="mass",
        mask_dir=File.sample(),
        warp_dir=False,
        transformed_dir=False,
        linear_transformations_dir=False,
        template_mask=False,
        noreorientation=True,
        leave_one_out="0",
        aggregate="mean",
        aggregation_weights=File.sample(),
        nanmask=True,
        copy_input=True,
        delete_temporary_files=True,
        nl_scale=list([1.0]),
        nl_lmax=list([1]),
        nl_niter=list([1]),
        nl_update_smooth=1.0,
        nl_disp_smooth=1.0,
        nl_grad_step=1.0,
        linear_no_pause=True,
        linear_no_drift_correction=True,
        linear_estimator="l1",
        rigid_scale=list([1.0]),
        rigid_lmax=list([1]),
        rigid_niter=list([1]),
        affine_scale=list([1.0]),
        affine_lmax=list([1]),
        affine_niter=list([1]),
        mc_weight_initial_alignment=list([1.0]),
        mc_weight_rigid=list([1.0]),
        mc_weight_affine=list([1.0]),
        mc_weight_nl=list([1.0]),
        nocleanup=True,
        scratch=False,
        cont=File.sample(),
        debug=True,
        force=True,
    )
    result = task(plugin="serial")
    assert not result.errored
