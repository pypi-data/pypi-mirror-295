"""
Projection between surface, volume and hybrid spaces
"""

import multiprocessing as mp
import os
from collections import defaultdict
from textwrap import dedent
import functools

import h5py
import numpy as np
from scipy import sparse
from regtricks import ImageSpace

from toblerone import surface_estimators, utils
from toblerone.classes import Hemisphere, Surface
from toblerone.core import vox_tri_weights, vtx_tri_weights

SIDES = ["L", "R"]


class Structure:
    """
    Lightweight class for each anatomical structure in a projector.
    Stores the PVs and forward/reverse projection matrices.
    """

    def __init__(self, n2v, v2n, pvs, name):
        self.n2v = sparse.csr_matrix(n2v)
        self.v2n = sparse.csr_matrix(v2n)
        assert pvs.ndim == 3
        self.pvs = pvs
        self.name = name
        self.n_nodes = n2v.shape[1]

    @property
    def n2v_noedge(self):
        return utils.sparse_normalise(self.n2v, 1)


class Projector(object):
    """
    Use to perform projection between volume, surface and node space.
    Creating a projector object may take some time whilst the consituent
    matrices are prepared; once created any of the individual projections
    may be calculated directly from the object.

    Node space ordering: L hemisphere surface, R hemisphere surface,
    brain voxels voxels in linear index order, ROIs in alphabetical
    order according to their dictionary key (see below)

    WARNING: surfaces must be in alignment before calling this function - ie,
    apply all registrations beforehand.

    Args:
        ref (str/ImageSpace): path for, or ImageSpace object, for reference voxel grid
        struct2ref (np.array): affine transformation from surface to reference space
        hemispheres (list/Hemisphere): single or list (L/R) of Hemisphere objects.
        nonbrain_pvs (np.array): non-brain PV estimates in reference voxel grid
        rois_pvs (dict): ROIs; keys are ROI name and values
            are volumetric PV maps representing ROI fraction.
        cores (int): number of processor cores to use (default max)
        ones (bool): debug tool, whole voxel PV assignment.
    """

    def __init__(
        self,
        ref,
        struct2ref,
        hemispheres,
        nonbrain_pvs=None,
        roi_pvs={},
        cores=mp.cpu_count(),
        ones=False,
    ):
        if not isinstance(ref, ImageSpace):
            self.spc = ImageSpace(ref)
        else:
            self.spc = ref

        if isinstance(hemispheres, Hemisphere):
            hemispheres = [hemispheres]

        self.structures = {}
        self.hemi_dict = {h.side: h for h in hemispheres}
        self.roi_names = list(roi_pvs.keys())
        roi_pvs = {**roi_pvs}

        # Append subcortical ROIs
        for k, v in roi_pvs.items():
            if not (k.startswith("L_") or k.startswith("R_")):
                raise ValueError(
                    "All subcortical ROIs must have keys starting with L_ or R_"
                )

            if not np.all(v.shape == self.spc.size):
                raise ValueError(
                    f"PVs for ROI {k} do not have same shape "
                    f"as reference space {v.shape} vs {self.spc.size}"
                )

        factor = 2 * np.ceil(self.spc.vox_size).astype(int)
        for s in self.hemi_dict.keys():
            h = self.hemi_dict[s].transform(struct2ref)
            h.pvs = surface_estimators.cortex(
                h,
                self.spc,
                np.eye(4),
                supr=2 * np.ceil(self.spc.vox_size).astype(int),
                cores=cores,
                ones=ones,
            )
            self.hemi_dict[s] = h

        # Calculate mappings between vertices and triangles,
        # then triangles and voxels
        worker = functools.partial(vox_tri_weights, spc=ref, factor=factor, ones=ones)
        surfs = [h.surfs for h in self.hemi_dict.values()]
        mid = [h.midsurface() for h in self.hemi_dict.values()]

        c = min(len(surfs), cores)
        if c > 1:
            with mp.Pool(c) as p:
                vox_tri_result = p.starmap(worker, surfs)
                vtx_tri_result = p.map(vtx_tri_weights, mid)
        else:
            vox_tri_result = [worker(*s) for s in surfs]
            vtx_tri_result = [vtx_tri_weights(m) for m in mid]

        for s, vox_tri, vtx_tri in zip(
            self.hemi_dict.keys(), vox_tri_result, vtx_tri_result
        ):
            self.hemi_dict[s].vox_tri = vox_tri
            self.hemi_dict[s].vtx_tri = vtx_tri

        # Global GM scaling - ensure GM PV never above 1
        all_gm_pv = np.stack(
            [
                *[self.hemi_dict[s].pvs[..., 0] for s in self.hemi_dict.keys()],
                *[roi_pvs[r] for r in self.roi_names],
            ],
            axis=-1,
        )
        all_gm_pv_sum = all_gm_pv.sum(-1)
        to_scale = all_gm_pv_sum > 1
        np.divide(
            all_gm_pv,
            all_gm_pv_sum[..., None],
            where=to_scale[..., None],
            out=all_gm_pv,
        )
        idx = 0
        for s in self.hemi_dict.keys():
            # GM PV may be decreased here, in which case re-assign to WM
            delta_gm = self.hemi_dict[s].pvs[..., 0] - all_gm_pv[..., idx]
            x = self.hemi_dict[s].pvs
            x[..., 0] -= delta_gm
            x[..., 1] += delta_gm
            assert np.allclose(x.sum(-1), 1, atol=1e-3)
            self.hemi_dict[s].pvs = x
            idx += 1
        for r in self.roi_names:
            roi_pvs[r] = all_gm_pv[..., idx]
            idx += 1

        # Get the cortical PVs
        if len(self.hemi_dict) > 1:
            # Combine PV estimates from each hemisphere into single map
            cpvs = np.zeros((*self.spc.size, 3))
            cpvs[..., 0] = np.minimum(
                1.0, self.hemi_dict["L"].pvs[..., 0] + self.hemi_dict["R"].pvs[..., 0]
            )
            cpvs[..., 1] = np.minimum(
                1.0 - cpvs[..., 0],
                self.hemi_dict["L"].pvs[..., 1] + self.hemi_dict["R"].pvs[..., 1],
            )
            cpvs[..., 2] = 1.0 - cpvs[..., 0:2].sum(-1)
        else:
            cpvs = next(iter(self.hemi_dict.values())).pvs
        self.cortex_pvs = cpvs

        # Update non-brain PVs using cortical PV mask (enforces single-hemisphere mode)
        if nonbrain_pvs is None:
            nonbrain_pvs = self.cortex_pvs[..., 2]
        else:
            if not np.all(nonbrain_pvs.shape == self.spc.size):
                raise ValueError(
                    f"Nonbrain PVs do not have same shape as reference "
                    f"space {nonbrain_pvs.shape} vs {self.spc.size}"
                )
            ctx_mask = self.cortex_pvs[..., :2].any(-1)
            nonbrain_pvs[~ctx_mask] = 1

        # Calculate the final PV maps
        to_stack = defaultdict(lambda: np.zeros(cpvs.shape[:3]))
        to_stack.update(
            {
                "cortex_GM": cpvs[..., 0],
                "cortex_WM": cpvs[..., 1],
                "cortex_nonbrain": cpvs[..., 2],
                "nonbrain": nonbrain_pvs,
                **roi_pvs,
            }
        )
        all_pvs = utils.stack_images(to_stack)
        self.pvs = all_pvs

        # Create all projector structures
        # Cortex
        for s, h in self.hemi_dict.items():
            v2n = assemble_vol2surf(h.vox_tri, h.vtx_tri)
            n2v = assemble_surf2vol(h.vox_tri, h.vtx_tri).tocsc()
            n2v.data *= np.take(h.pvs[..., 0], n2v.indices)
            self.structures[f"{s}_cortex"] = Structure(
                n2v=n2v, v2n=v2n, pvs=h.pvs[..., 0], name=f"{s}_cortex"
            )

        # WM
        wm_pv = all_pvs[..., 1]
        n2v = sparse.diags(wm_pv.flatten(), 0)
        v2n = sparse.eye(n2v.shape[0])
        self.structures["WM"] = Structure(n2v=n2v, v2n=v2n, pvs=wm_pv, name="WM")

        # Subcortical ROIs
        for r, v in roi_pvs.items():
            n2v = sparse.diags(v.flatten(), 0)
            v2n = sparse.eye(n2v.shape[0])
            self.structures[r] = Structure(n2v=n2v, v2n=v2n, pvs=v, name=r)

    def save(self, path):
        """
        Save Projector in HDF5 format.

        A projector can be re-used for multiple analyses, assuming the reference
        image space and cortical surfaces remain in alignment for all data.

        Args:
            path (str): path to write out with .h5 extension
        """

        ctype = "gzip"

        def write_sparse(spmat, name, g):
            # Sparse matrices cannot be save in HDF5, so convert them
            # to COO and then save as a 3 x N array, where the top row
            # is row indices, second is columns, and last is data.
            spmat = spmat.tocoo()
            shp = spmat.shape
            spmat = np.vstack((spmat.row, spmat.col, spmat.data), dtype=utils.NP_FLOAT)
            g.create_dataset(name, data=spmat, compression=ctype)
            g.create_dataset(f"{name}_shape", data=shp)

        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with h5py.File(path, "w") as f:
            # Save properties of the reference ImageSpace: vox2world, size
            # and filename
            f.create_dataset("ref_spc_vox2world", data=self.spc.vox2world)
            f.create_dataset("ref_spc_size", data=self.spc.size)
            if self.spc.fname:
                f.create_dataset(
                    "ref_spc_fname",
                    data=np.array(self.spc.fname.encode("utf-8")),
                    dtype=h5py.string_dtype("utf-8"),
                )

            f.create_dataset("cortex_pvs", data=self.cortex_pvs, compression=ctype)
            f.create_dataset("pvs", data=self.pvs, compression=ctype)

            # Each hemisphere is a group within the file (though there may
            # only be 1)
            for h in self.iter_hemis:
                side = h.side
                g = f.create_group(f"{side}_hemi")

                # Save the surfaces of each hemisphere, named
                # as LPS,RPS,LWS,RWS.
                for k, s in h.surf_dict.items():
                    g.create_dataset(f"{k}_tris", data=s.tris, compression=ctype)
                    g.create_dataset(f"{k}_points", data=s.points, compression=ctype)

            # Save each structure
            g = f.create_group("structures")
            for n, s in self.structures.items():
                g2 = g.create_group(n)
                write_sparse(s.n2v, "n2v", g2)
                write_sparse(s.v2n, "v2n", g2)
                g2.create_dataset("pvs", data=s.pvs, compression=ctype)

    @classmethod
    def load(cls, path):
        """
        Load Projector from path in HDF5 format.

        This is useful for performing repeated analyses with the same voxel
        grid and cortical surfaces.

        Args:
            path (str): path to load from
        """

        def load_sparse(grp, name):
            # Load a sparse matrix from a 3 x N array
            spmat = grp[name][()]
            shp = grp[f"{name}_shape"][()]
            return sparse.coo_matrix(
                (spmat[2, :], (spmat[0, :].astype(int), spmat[1, :].astype(int))),
                shape=shp,
            ).tocsr()

        with h5py.File(path, "r") as f:
            p = cls.__new__(cls)

            # Recreate the reference ImageSpace first
            p.spc = ImageSpace.manual(f["ref_spc_vox2world"][()], f["ref_spc_size"][()])
            if "ref_spc_fname" in f:
                fname = f["ref_spc_fname"][()]
                if isinstance(fname, bytes):
                    fname = fname.decode("utf-8")
                p.spc.fname = fname

            # Now read out hemisphere specific properties
            p.hemi_dict = {}
            p.structures = {}
            p.cortex_pvs = f["cortex_pvs"][()]
            p.pvs = f["pvs"][()]

            for s in SIDES:
                hemi_key = f"{s}_hemi"
                if hemi_key in f:
                    # Read out the surfaces, create the Hemisphere
                    ins, outs, sph = [
                        Surface.manual(
                            f[hemi_key][f"{s}{n}S_points"][()],
                            f[hemi_key][f"{s}{n}S_tris"][()],
                            f"{s}{n}S",
                        )
                        for n in ["W", "P", "S"]
                    ]
                    p.hemi_dict[s] = Hemisphere(ins, outs, sph, s)

            g = f["structures"]
            for k in sorted(g.keys()):
                n2v = load_sparse(g[k], "n2v")
                v2n = load_sparse(g[k], "v2n")
                p.structures[k] = Structure(n2v, v2n, g[k]["pvs"][()], k)

            return p

    def __repr__(self):
        nstructs = len(self.structures)
        spc = "\n".join(repr(self.spc).splitlines()[1:])
        disp = dedent(
            f"""\
        Projector for {nstructs} structures: {self.structure_names}.
        Reference voxel grid:"""
        )
        return disp + "\n" + spc

    @property
    def iter_hemis(self):
        """Iterator over hemispheres of projector, in L/R order"""

        for s in SIDES:
            if s in self.hemi_dict:
                yield self.hemi_dict[s]

    @property
    def structure_names(self):
        return list(self.structures.keys())

    @property
    def n_hemis(self):
        """Number of hemispheres (1/2) in projector"""

        return len(self.hemi_dict)

    @property
    def n_structures(self):
        """Number of structures in projector"""

        return len(self.structures)

    # Direct access to the underlying surfaces via keys LPS, RWS etc.
    def __getitem__(self, surf_key):
        side = surf_key[0]
        return self.hemi_dict[side].surf_dict[surf_key]

    def adjacency_matrix(self):
        """
        Adjacency matrix for all surface vertices of projector.

        If there are two hemispheres present, the matrix indices will
        be arranged L,R.

        Returns:
            sparse CSR matrix, square sized (n vertices)
        """

        mats = []
        for hemi in self.iter_hemis:
            midsurf = hemi.midsurface()
            a = midsurf.adjacency_matrix().tolil()
            verts_vox = utils.affine_transform(
                midsurf.points, self.spc.world2vox
            ).round()
            verts_in_spc = ((verts_vox >= 0) & (verts_vox < self.spc.size)).all(-1)
            a[~verts_in_spc, :] = 0
            a[..., ~verts_in_spc] = 0
            mats.append(a)

        return sparse.block_diag(mats, format="csr")

    def brain_mask(self, pv_threshold=0.1):
        """Boolean mask of brain voxels, in reference ImageSpace

        Args:
            pv_threshold (float): minimum brain PV (WM+GM) to include

        Returns:
            np.array, same shape as reference space, boolean dtype
        """

        return self.cortex_pvs[..., :2].sum(-1) > pv_threshold

    def to_nodes(self, voxel_data, structs=None):
        """
        Project voxel-wise data to the nodes of each structure

        Args:
            voxel_data (np.array): 3D data in voxel space
            structs (list): list of structures to project to. Default is all structures.

        Returns:
            dict: dict of projected data for each structure, keyed by structure name
        """

        if not structs:
            structs = self.structures.keys()

        x = {s: self.structures[s].v2n @ voxel_data.flatten() for s in structs}
        return x

    def to_voxels(self, struct_data, edge_scale=True):
        """
        Project node-wise data to voxels

        Args:
            struct_data (dict): 1D node-wise data keyed by structure name
            edge_scale (bool): downweight voxel data by structure PV

        Returns:
            np.array 3D voxel-wise data
        """

        structs = struct_data.keys()
        n2v = sparse.hstack([self.structures[s].n2v for s in structs])
        if not edge_scale:
            n2v = utils.sparse_normalise(n2v, 1)

        vec = np.concatenate([struct_data[s].flatten() for s in structs])
        x = n2v @ vec
        return x.reshape(self.spc.size)


def assemble_vol2surf(vox_tri, vtx_tri):
    """
    Combine with normalisation the vox_tri and vtx_tri matrices into vol2surf.
    """

    # Ensure each triangle's voxel weights sum to 1
    # Ensure each vertices' triangle weights sum to 1
    vox2tri = utils.sparse_normalise(vox_tri, 0).T
    tri2vtx = utils.sparse_normalise(vtx_tri, 1)
    vol2vtx = tri2vtx @ vox2tri
    return utils.sparse_normalise(vol2vtx, 1)


def assemble_surf2vol(vox_tri, vtx_tri):
    """
    Combine with normalisation the vox_tri and vtx_tri matrices into surf2vol.
    """

    # Ensure each triangle's vertex weights sum to 1
    # Ensure each voxel's triangle weights sum to 1
    vtx2tri = utils.sparse_normalise(vtx_tri, 0).T
    tri2vox = utils.sparse_normalise(vox_tri, 1)
    vtx2vox = tri2vox @ vtx2tri
    return utils.sparse_normalise(vtx2vox, 1)
