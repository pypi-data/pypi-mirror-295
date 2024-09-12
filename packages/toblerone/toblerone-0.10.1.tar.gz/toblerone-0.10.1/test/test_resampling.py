import os.path as op
import numpy as np
import toblerone as tob
from toblerone import utils
import nibabel as nib


def get_testdir():
    return op.dirname(__file__)


def test_resample_hemisphere():
    td = get_testdir() + "/testdata/native"
    LWS = op.join(td, "lh.white")
    LPS = op.join(td, "lh.pial")
    LSS = op.join(td, "lh.sphere")

    hemi = tob.Hemisphere(LWS, LPS, LSS, "L")
    h2 = hemi.resample_geometry(n_verts=64000)


def test_resample_surface():
    td = get_testdir() + "/testdata/native"
    LWS = tob.Surface(op.join(td, "lh.white"), "LWS")
    LSS = tob.Surface(op.join(td, "lh.sphere"), "LSS")
    l1, sph = LWS.resample_geometry(LSS, n_verts=64000)
    l2, sph2 = l1.resample_geometry(sph, new_sphere=LSS)

    assert np.allclose(LWS.points.min(0), l1.points.min(0), atol=1)
    assert np.allclose(LWS.points.max(0), l1.points.max(0), atol=1)
    assert (np.abs(LWS.points - l2.points).mean(0) < 0.1).all()


def test_resample_surfaces():
    td = get_testdir() + "/testdata/native"
    LWS = tob.Surface(op.join(td, "lh.white"), "LWS")
    LPS = tob.Surface(op.join(td, "lh.pial"), "LPS")
    LSS = tob.Surface(op.join(td, "lh.sphere"), "LSS")

    utils.resample_surfaces([LWS, LPS], LSS, n_verts=64000)


def test_resample_metric():
    td = get_testdir() + "/testdata/native"
    LSS = tob.Surface(op.join(td, "lh.sphere"), name="LSS")
    thick = nib.freesurfer.read_morph_data(op.join(td, "lh.thickness"))

    t1, low_sph = utils.resample_metric(thick, LSS, n_verts=64000)
    t2, _ = utils.resample_metric(t1, low_sph, new_sphere=LSS)

    assert np.allclose(thick.min(), t1.min(), atol=1)
    assert np.allclose(thick.max(), t1.max(), atol=1)
    assert np.abs(thick - t2).mean() < 0.1


if __name__ == "__main__":
    test_resample_surfaces()
    test_resample_surface()
    test_resample_hemisphere()
    test_resample_metric()
