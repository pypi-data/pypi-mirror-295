import os
import numpy as np
from scipy import sparse
import regtricks as rt
import toblerone as tob
from toblerone import core, icosphere, utils
import trimesh


PS, TS = icosphere.icosphere(nr_verts=1000)
PS = PS.astype(utils.NP_FLOAT)
TS = TS.astype(utils.NP_INT)
UNIT_SPHERE = tob.Surface.manual(PS, TS, "unit_sphere")
ENCL_SPACE = rt.ImageSpace.create_axis_aligned([-1, -1, -1], [2, 2, 2], [1, 1, 1])


def test_surface_create():
    ps, ts = icosphere.icosphere(nr_verts=1000)
    surf = tob.Surface.manual(ps, ts, "lss")
    assert np.allclose(ps, surf.points), "surface vertices are not equal"
    assert np.allclose(ts, surf.tris), "surface triangles are not equal"


def test_subvoxels():
    vox_cent = np.random.randint(-10, 10, 3)

    supr = np.random.randint(2, 3, 3)
    subvox_size = 1.0 / supr
    subvox_cents = core._get_subvoxel_grid(supr) + vox_cent
    assert subvox_cents.shape[0] == supr.prod()

    mean_cent = subvox_cents.mean(0)
    assert np.allclose(mean_cent, vox_cent), "subvoxels not evenly distributed"
    assert np.allclose(
        subvox_cents.max(0) - vox_cent, subvox_size / 2
    ), "dist to furthest subvoxel not equal to subvoxel size / 2"
    assert np.allclose(
        subvox_cents.min(0) - vox_cent, -subvox_size / 2
    ), "dist to closest subvoxel not equal to -subvoxel size / 2"


def test_singl1e_intersection():
    ps = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]).astype(utils.NP_FLOAT)
    ts = np.array([[0, 1, 2], [0, 2, 3]]).astype(utils.NP_INT)
    ray = np.array([0, 0, 1]).astype(utils.NP_FLOAT)
    xprods = np.array([[0, 0, 1], [0, 0, 1]]).astype(utils.NP_FLOAT)
    root1 = np.array([0.5, 0.5, -1]).astype(utils.NP_FLOAT)
    root2 = np.array([0.5, 0.5, 1]).astype(utils.NP_FLOAT)

    mu = core._findRayTriangleIntersections3D(root1, ray, ps, ts, xprods)
    assert len(mu) == 1, "ray should intersect exactly one triangle"
    assert np.allclose(mu[0], 1.0), "ray should intersect at z=1"

    mu = core._findRayTriangleIntersections3D(root2, ray, ps, ts, xprods)
    assert len(mu) == 1, "ray should intersect exactly one triangle"
    assert np.allclose(mu[0], -1.0), "ray should intersect at z=-1"


def test_sph_intersections():
    root = np.array([0, 0, 0]).astype(utils.NP_FLOAT)
    rays = np.random.normal(size=(10000, 3)).astype(utils.NP_FLOAT)
    xp = trimesh.Trimesh(vertices=PS, faces=TS).face_normals
    for ray in rays:
        mu = core._findRayTriangleIntersections3D(root, ray, PS, TS, xp)
        assert len(mu) == 2, "ray should intersect exactly two triangles"
        assert np.allclose(mu[0], -mu[1]), "intersection points should be symmetric"


def test_points_in_tetra():
    tet = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1]]).astype(np.float64)
    vol = 1 / 3 * (0.5) * 1  # 1/3 * base * height
    points = np.random.uniform(0, 1.000001, size=(100_000, 3))
    test = core.test_points_in_tetra(points, tet)
    assert np.allclose(
        test.mean(), vol, atol=1e-2
    ), "proportion of points in tetrahedron does not match volume"


def test_points_in_prism():
    in_surf = tob.Surface.manual(
        np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0]]), np.array([[0, 1, 2]]), "LWS"
    )
    out_surf = tob.Surface.manual(
        np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1]]), np.array([[0, 1, 2]]), "LWS"
    )
    spc = rt.ImageSpace.create_axis_aligned([0, 0, 0], [1, 1, 1], [1, 1, 1])
    factor = 20 * np.ones(3, dtype=int)
    vox_tri_weights = core.vox_tri_weights(in_surf, out_surf, spc, factor, False)
    assert vox_tri_weights.nnz == 1, "vox_tri_weights should have 1 non-zero element"
    assert np.allclose(
        vox_tri_weights.data[0] / factor.prod(), 0.5
    ), "vox_tri_weights should be 0.5"


def test_intersection_distance():
    root = np.array([0, 0, 0]).astype(utils.NP_FLOAT)
    ray = np.array([0, 0, 1]).astype(utils.NP_FLOAT)
    xp = trimesh.Trimesh(vertices=PS, faces=TS).face_normals
    mu = core._findRayTriangleIntersections3D(root, ray, PS, TS, xp)
    mu = sorted(mu)
    assert np.allclose(mu[0], -1), "first intersection should be at z=-1"
    assert np.allclose(mu[1], 1), "second intersection should be at z=1"

    root = np.array([0, 0, -1]).astype(utils.NP_FLOAT)
    mu = core._findRayTriangleIntersections3D(root, ray, PS, TS, xp)
    mu = sorted(mu)
    assert np.allclose(mu[0], 0), "first intersection should be at z=-1"
    assert np.allclose(mu[1], 2), "second intersection should be at z=1"


def test_write_read_surface_vtk():
    ps, ts = icosphere.icosphere(nr_verts=1000)
    s = tob.Surface.manual(ps, ts, "lss")
    s.save("test.vtk")
    s2 = tob.Surface("test.vtk", "LSS")
    assert np.allclose(s.points, s2.points)
    os.remove("test.vtk")


def test_sparse_normalise():
    mat = sparse.random(5000, 5000, 0.1)
    thr = 1e-12
    for axis in range(2):
        normed = utils.sparse_normalise(mat, axis, thr)
        sums = normed.sum(axis).A.flatten()
        assert (np.abs(sums[sums > 0] - 1) <= thr).all()


def test_hemi_init():
    ps, ts = icosphere.icosphere(nr_verts=1000)
    ins = tob.Surface.manual(ps, ts, "lws")
    sph = tob.Surface.manual(ps, ts, "lss")
    outs = tob.Surface.manual(ps * 2, ts, "lps")
    hemi = tob.Hemisphere(ins, outs, sph, "L")
    hemi2 = tob.Hemisphere(ins, outs, sph, "L")
    assert id(hemi.inSurf) != id(hemi2.inSurf)
    assert np.allclose(hemi.outSurf.tris, hemi.outSurf.tris)


if __name__ == "__main__":
    test_intersection_distance()
