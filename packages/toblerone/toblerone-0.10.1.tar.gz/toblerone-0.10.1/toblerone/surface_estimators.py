# Functions to estimate the PVs of the cerebral cortex and subcortical
# structures. These are wrappers around the core Toblerone functions
# that handle the aggregate various pieces of information into overall results

import copy
import warnings
from functools import partial
import multiprocessing as mp

import numpy as np

from toblerone import utils, core


def cortex(hemispheres, space, struct2ref, supr, cores, ones):
    """
    Estimate the PVs of the cortex.

    Args:
        hemispheres: either a single, or iterable list of, Hemisphere objects.
        space: an ImageSpace within which to operate.
        struct2ref: np.array affine transformation into reference space.
        supr: supersampling factor (3-vector) to use for estimation.
        cores: number of processor cores to use.
        ones: debug tool, write ones in all voxels containing triangles.

    Returns:
        4D array, size equal to the reference image, with the PVs arranged
            GM/WM/non-brain in 4th dim
    """

    if not isinstance(hemispheres, list):
        hemispheres = [hemispheres]
    else:
        hemispheres = [copy.deepcopy(h) for h in hemispheres]

    for idx in range(len(hemispheres)):
        h = hemispheres[idx].transform(struct2ref)
        if np.any(np.max(np.abs(h.inSurf.points)) > np.max(np.abs(h.outSurf.points))):
            warnings.warn(
                "Inner surface vertices appear to be further"
                + " from the origin than the outer vertices. Are the surfaces in"
                + " the correct order?"
            )
        hemispheres[idx] = h

    surfs = [s for h in hemispheres for s in h.surfs]
    func = partial(core.voxelise, space=space, factor=supr, binary=ones)
    if cores == 1:
        pvs_surf = list(map(func, surfs))
    else:
        with mp.Pool(min(cores, len(surfs))) as pool:
            pvs_surf = pool.map(func, surfs)
    for s, pvs in zip(surfs, pvs_surf):
        s.pvs = pvs.flatten()

    # Merge the inner/outer surface PVs
    for h in hemispheres:
        in_pvs = h.inSurf.pvs
        out_pvs = h.outSurf.pvs

        # Combine estimates from each surface into whole hemi PV estimates
        hemiPVs = np.zeros((np.prod(space.size), 3), dtype=utils.NP_FLOAT)
        hemiPVs[:, 1] = in_pvs
        hemiPVs[:, 0] = np.maximum(0.0, out_pvs - in_pvs)
        hemiPVs[:, 2] = 1.0 - (hemiPVs[:, 0:2].sum(1))
        h.PVs = hemiPVs

    # Merge the hemispheres, giving priority to GM, then WM, then CSF.
    # Do nothing if just one hemi
    if len(hemispheres) == 1:
        outPVs = hemispheres[0].PVs

    else:
        h1, h2 = hemispheres
        outPVs = np.zeros((np.prod(space.size), 3), dtype=utils.NP_FLOAT)
        outPVs[:, 0] = np.minimum(1.0, h1.PVs[:, 0] + h2.PVs[:, 0])
        outPVs[:, 1] = np.minimum(
            np.maximum(1.0 - outPVs[:, 0], 0), h1.PVs[:, 1] + h2.PVs[:, 1]
        )
        outPVs[:, 2] = 1.0 - outPVs[:, 0:2].sum(1)

    # Sanity checks
    if np.any(outPVs > 1.0):
        raise RuntimeError("PV exceeds 1")

    if np.any(outPVs < 0.0):
        raise RuntimeError("Negative PV returned")

    if not np.all(outPVs.sum(1) == 1.0):
        raise RuntimeError("PVs do not sum to 1")

    return outPVs.reshape((*space.size, 3))


def structure(surf, space, struct2ref, supr, ones):
    """
    Estimate the PVs of a structure denoted by a single surface. Note
    that the results should be interpreted simply as "fraction of each
    voxel lying within the structure", and it is ambiguous as to what tissue
    lies outside the structure

    Args:
        surf: Surface object
        space: ImageSpace to estimate within
        struct2ref: np.array affine transformation into reference space.
        supr: supersampling factor (3-vector) to use for estimation
        ones: debug tool, write ones in voxels containing triangles
        cores: number of processor cores to use

    Returns:
        an array of size refSpace.size containing the PVs.
    """

    # Create our own local copy of inputs
    loc_surf = copy.deepcopy(surf)
    loc_surf = loc_surf.transform(struct2ref)
    pvs = core.voxelise(loc_surf, space, supr, ones)

    return pvs
