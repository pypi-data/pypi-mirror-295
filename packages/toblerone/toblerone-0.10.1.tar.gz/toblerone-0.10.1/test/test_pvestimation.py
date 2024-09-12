"""Toblerone tests"""

import os.path as op
import numpy as np
import regtricks as rt
import trimesh

import toblerone as tob
from toblerone import icosphere, utils, core


PS, TS = icosphere.icosphere(nr_verts=1000)
PS = PS.astype(utils.NP_FLOAT)
TS = TS.astype(utils.NP_INT)
UNIT_SPHERE = tob.Surface.manual(PS, TS, "unit_sphere")
ENCL_SPACE = rt.ImageSpace.create_axis_aligned([-1, -1, -1], [2, 2, 2], [1, 1, 1])

# TODO test with partial FoV


def get_testdir():
    return op.dirname(__file__)


def test_sph_partial_voxelise():
    half_space = ENCL_SPACE.resize([0, 0, 0], [1, 2, 2])
    ps_vox = rt.aff_trans(half_space.world2vox, PS)
    mesh_vox = trimesh.Trimesh(vertices=ps_vox, faces=TS)
    vox = tob.core.binary_voxelise(mesh_vox, half_space)
    assert np.all(vox.shape == half_space.size)
    assert vox.all(), "all voxels centres lie within half sphere"

    spc2 = half_space.resize_voxels(0.05)
    ps_vox = rt.aff_trans(spc2.world2vox, PS)
    mesh_vox = trimesh.Trimesh(vertices=ps_vox, faces=TS)
    vox2 = tob.core.binary_voxelise(mesh_vox, spc2)
    vol = 4 * vox2.sum() / vox2.size
    assert np.allclose(
        vol, 0.5 * 4 * np.pi / 3, rtol=0.05
    ), "voxelised volume not equal to ground truth"


def test_sph_voxelise():
    ps_vox = rt.aff_trans(ENCL_SPACE.world2vox, PS)
    mesh_vox = trimesh.Trimesh(vertices=ps_vox, faces=TS)
    vox = tob.core.binary_voxelise(mesh_vox, ENCL_SPACE)
    assert np.all(vox.shape == ENCL_SPACE.size)
    assert vox.all(), "all voxels centres lie within sphere"

    spc2 = ENCL_SPACE.resize_voxels(0.05)
    ps_vox = rt.aff_trans(spc2.world2vox, PS)
    mesh_vox = trimesh.Trimesh(vertices=ps_vox, faces=TS)
    vox2 = tob.core.binary_voxelise(mesh_vox, spc2)
    vol = 8 * vox2.sum() / vox2.size
    assert np.allclose(
        vol, 4 * np.pi / 3, rtol=0.05
    ), "voxelised volume not equal to ground truth"


def test_sph_pvs():
    pvs = core.voxelise(UNIT_SPHERE, ENCL_SPACE, [10, 10, 10])
    assert np.allclose(
        pvs.sum(), 4 * np.pi / 3, rtol=0.05
    ), "voxelised volume not equal to ground truth"


def test_sph_partial_pvs():
    half_space = ENCL_SPACE.resize([0, 0, 0], [1, 2, 2])
    pvs = core.voxelise(UNIT_SPHERE, half_space, [10, 10, 10])
    assert np.allclose(
        pvs.sum(), 0.5 * 4 * np.pi / 3, rtol=0.05
    ), "voxelised volume not equal to ground truth"


def test_cortex():
    spc = rt.ImageSpace.create_axis_aligned([-2, -2, -2], [4, 4, 4], [1, 1, 1])
    sph = tob.Surface.manual(PS, TS, "LSS")
    ins = tob.Surface.manual(1 * PS, TS, "LWS")
    outs = tob.Surface.manual(2 * PS, TS, "LPS")

    s2r = np.identity(4)
    supr = np.full(3, 10, dtype=int)
    fracs = tob.scripts.pvs_cortex_freesurfer(
        LWS=ins, LPS=outs, LSS=sph, ref=spc, struct2ref=s2r, supr=supr, cores=1
    )

    wm = fracs[..., 1].sum()
    gm = fracs[..., 0].sum()

    wm_true = 4 * np.pi * (1**3) / 3
    gm_true = (4 * np.pi * (2**3) / 3) - wm_true

    assert np.allclose(wm, wm_true, rtol=0.05)
    assert np.allclose(gm, gm_true, rtol=0.05)

    # Symmetry of results in central voxels
    wm = fracs[..., 1][fracs[..., 1] > 0]
    assert np.allclose(wm[0], wm, rtol=0.01)

    gm = fracs[1:3, 1:3, 1:3, 0]
    assert np.allclose(gm[0, 0, 0], gm, rtol=0.01)

    csf = fracs[1:3, 1:3, 1:3, 2]
    assert np.allclose(csf[0, 0, 0], 0, rtol=0.01)


def test_structure():
    spc = rt.ImageSpace.create_axis_aligned([-1, -1, -1], [2, 2, 2], [1, 1, 1])
    ps, ts = icosphere.icosphere(nr_verts=1000)
    sph = tob.Surface.manual(ps, ts, "struct")
    s2r = np.identity(4)

    fracs = tob.scripts.pvs_structure(surf=sph, ref=spc, struct2ref=s2r, supr=10)
    true = 4 * np.pi / 3
    assert np.allclose(fracs.sum(), true, rtol=0.05), "pvs do not sum to ground truth"
    assert np.allclose(
        fracs[0, 0, 0], fracs, rtol=0.01
    ), "pvs not symmetrically distributed across sphere"


def test_pvs_subcortex_freesurfer():
    td = get_testdir()

    spc = rt.ImageSpace(op.join(td, "testdata/T1_fast_pve_0.nii.gz"))
    spc = spc.resize_voxels(3)
    _ = tob.scripts.pvs_subcortex_freesurfer(
        ref=spc, struct2ref=np.eye(4), fsdir=op.join(td, "testdata/fs")
    )


def test_pvs_subcortex_fsl():
    td = get_testdir()
    td = op.join(td, "testdata")
    spc = rt.ImageSpace(op.join(td, "T1_fast_pve_0.nii.gz"))
    spc = spc.resize_voxels(3)

    fastdir = td
    firstdir = op.join(td, "first_results")
    s2r = np.eye(4)

    _ = tob.scripts.pvs_subcortex_fsl(
        ref=spc, struct2ref=s2r, firstdir=firstdir, fastdir=fastdir
    )


if __name__ == "__main__":
    test_sph_partial_voxelise()
