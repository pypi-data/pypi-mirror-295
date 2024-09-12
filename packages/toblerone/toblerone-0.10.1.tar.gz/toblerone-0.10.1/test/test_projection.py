import os
import tempfile
import numpy as np
import regtricks as rt
import toblerone as tob
from toblerone import core, icosphere

SPC = rt.ImageSpace.create_axis_aligned([-2, -2, -2], [10, 10, 10], [0.4, 0.4, 0.4])
ps, ts = icosphere.icosphere(nr_verts=500)
LWS = tob.Surface.manual(1.5 * ps, ts, "LWS")
LPS = tob.Surface.manual(1.9 * ps, ts, "LPS")
LSS = tob.Surface.manual(ps, ts, "LSS")
SUBCORT = tob.Surface.manual(0.5 * ps, ts, "subcort")


def test_vox_tri():
    vox_tri = core.vox_tri_weights(LWS, LPS, SPC, 5, 1)
    assert np.all(vox_tri.sum(0) > 0)


def test_vox_tri_partial_fov():
    half_space = SPC.resize([0, 0, 0], [5, 10, 10])
    vox_tri = core.vox_tri_weights(LWS, LPS, half_space, 5, 1)
    assert np.all(vox_tri.sum(0) > 0)


def test_hemi_transform():
    hemi = tob.Hemisphere(LWS, LPS, LSS, "L")
    hemi2 = hemi.transform(np.eye(4))
    assert np.all(hemi2.inSurf.points == hemi.inSurf.points)

    t = np.random.randn(4, 4)
    t[3, :] = [0, 0, 0, 1]
    hemi3 = hemi.transform(t)
    assert not np.all(hemi3.inSurf.points == hemi.inSurf.points)


def test_sph_projector():
    hemi = tob.Hemisphere(LWS, LPS, LSS, "L")
    roi_pvs = {
        "L_subcort": tob.scripts.pvs_structure(
            ref=SPC, struct2ref=np.eye(4), surf=SUBCORT
        )
    }

    p = tob.Projector(SPC, np.eye(4), [hemi], roi_pvs=roi_pvs)
    assert np.all(
        p.structures["L_cortex"].n2v.sum(0) > 0
    ), "all surface vertices should map to a voxel"
    assert p.n_hemis == 1, "projector should only have one hemisphere"
    assert "L" in p.hemi_dict, "projector should contain L hemisphere"
    assert p["LPS"], "projector should expose dict access"

    with tempfile.TemporaryDirectory() as d:
        fname = os.path.join(d, "proj.h5")
        p.save(fname)
        tob.Projector.load(fname)

    ndata = {"L_cortex": 2 * np.ones(hemi.n_points), "L_subcort": np.ones(SPC.n_vox)}

    # node to volume
    eps = 1e-3
    n2v = p.to_voxels(ndata, False)
    n2v_pv = p.to_voxels(ndata, True)
    assert (n2v_pv <= n2v + eps).all(), "pv weighting did not reduce signal"

    for s in p.structure_names:
        assert p.structures[s].n2v.sum(1).max() < 1 + eps, "total voxel weight > 1"
        assert (
            p.structures[s].n2v_noedge.sum(1).max() < 1 + eps
        ), "total voxel weight > 1"
        assert p.structures[s].v2n.sum(1).max() < 1 + eps, "total node weight > 1"


def test_save_and_load_projector_hdf5():
    hemi = tob.Hemisphere(LWS, LPS, LSS, "L")
    proj = tob.Projector(SPC, np.eye(4), [hemi])
    proj.save("proj.h5")
    proj2 = tob.Projector.load("proj.h5")

    for s in proj.structure_names:
        assert np.array_equiv(
            proj.structures[s].pvs, proj2.structures[s].pvs
        ), "pvs were not preserved"
        assert np.array_equiv(
            proj.structures[s].n2v.todense(), proj2.structures[s].n2v.todense()
        ), "n2v matrix not preserved"
        assert np.array_equiv(
            proj.structures[s].v2n.todense(), proj2.structures[s].v2n.todense()
        ), "v2n matrix not preserved"

    os.remove("proj.h5")


def test_hemisphere_laplacian():
    hemi = tob.Hemisphere(LWS, LPS, LSS, "L")
    hemi.mesh_laplacian()


def test_adjacency():
    hemi = tob.Hemisphere(LWS, LPS, LSS, "L")
    adj = hemi.adjacency_matrix()
    assert not (adj.data < 0).any(), "negative value in adjacency matrix"


if __name__ == "__main__":
    test_vox_tri_partial_fov()
