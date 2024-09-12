"""
Surface-related classes
"""

import copy
import getpass
import os.path as op
import warnings
from datetime import datetime

import nibabel
import numpy as np
import pyvista
import regtricks as rt
import vtk
from scipy import sparse

from .. import core, utils, icosphere
from ..utils import NP_FLOAT, NP_INT


class Surface(object):
    """
    Encapsulates a surface's points, triangles and associations data.
    Create either by passing a file path (as below) or use the static class
    method Surface.manual() to directly pass points and triangles.

    Args:
        path (str): path to file (GIFTI/FS binary/pyvista compatible)
        name (str): optional, for progress bars
    """

    def __init__(self, path, name, shift_cras=True):
        if not op.exists(path):
            raise RuntimeError("File {} does not exist".format(path))

        # Can we get an extension please, makes life easier
        surfExt = op.splitext(path)[-1]

        # GIFTI via nibabel
        if surfExt == ".gii":
            try:
                gft = nibabel.load(path).darrays
                ps, ts = gft[0].data, gft[1].data

            except Exception as e:
                print(
                    f"""Could not load {path} as .gii. Is it a surface
                    GIFTI (.surf.gii)?"""
                )
                raise e

        # VTK via vtk (ie python vtk library)
        elif surfExt == ".vtk":
            try:
                reader = vtk.vtkGenericDataObjectReader()
                reader.SetFileName(path)
                reader.Update()

                ps = np.array(reader.GetOutput().GetPoints().GetData())
                ts = np.array(reader.GetOutput().GetPolys().GetData())

                # tris array is returned as a single vector eg
                # [3 a b c 3 a b c] where 3 represents triangle faces
                # so it actually has FOUR columns, the first of which
                # is all 3...
                if ts.size % 4:
                    raise ValueError(
                        f"VTK file does not appear to be triangle data (first poly has {ts[0]} faces"
                    )
                ts = ts.reshape(-1, 4)
                if (ts[:, 0] != 3).any():
                    raise ValueError(
                        f"VTK file does not appear to be triangle data (first poly has {ts[0,0]} faces"
                    )
                ts = ts[:, 1:]

            except Exception as e:
                print(
                    f"""Could not load {path} as .vtk. Is it a triangle
                    VTK?"""
                )
                raise e

        else:
            # FS files don't have a proper extension (binary)
            # FreeSurfer via nibabel
            try:
                ps, ts, meta = nibabel.freesurfer.io.read_geometry(
                    path, read_metadata=True
                )
                if shift_cras:
                    ps += meta["cras"]

            # Maybe FreeSurfer didn't work, try anything else via pyvista
            except Exception:
                try:
                    poly = pyvista.read(path)
                    ps = np.array(poly.points)
                    ts = poly.faces.reshape(-1, 4)[:, 1:]

                except Exception:
                    raise RuntimeError("Could not load surface via pyvista")

        if ps.shape[1] != 3:
            raise RuntimeError("Points matrices should be p x 3")

        if ts.shape[1] != 3:
            raise RuntimeError("Triangles matrices should be t x 3")

        if (np.max(ts) != ps.shape[0] - 1) or (np.min(ts) != 0):
            raise RuntimeError("Incorrect points/triangle indexing")

        # TODO could check closed and winding consistent here?

        self.points = ps.astype(NP_FLOAT)
        self.tris = ts.astype(NP_INT)
        self.name = name

    def __repr__(self):
        from textwrap import dedent

        return dedent(
            f"""\
            Surface with {self.n_points} points and {self.tris.shape[0]} triangles.
            min (X,Y,Z):  {self.points.min(0)}
            mid (X,Y,Z): {utils.find_sphere_centre(self.points)}
            max (X,Y,Z):  {self.points.max(0)}
            """
        )

    @classmethod
    def manual(cls, ps, ts, name):
        """Manual surface constructor using points and triangles arrays"""

        if (ps.shape[1] != 3) or (ts.shape[1] != 3):
            raise RuntimeError("ps, ts arrays must have N x 3 dimensions")

        if ts.min() > 0:
            raise RuntimeError("ts array should be 0-indexed")

        s = cls.__new__(cls)
        s.points = copy.deepcopy(ps.astype(NP_FLOAT))
        s.tris = copy.deepcopy(ts.astype(NP_INT))
        s.name = name
        return s

    @property
    def n_points(self):
        return self.points.shape[0]

    def to_metric(self, data):
        """Return vertex-wise data as GIFTI functional object"""

        from .._version import __version__

        if not self.n_points == data.shape[0]:
            raise RuntimeError("Incorrect data shape")

        meta = {
            "UserName": getpass.getuser(),
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Description": f"Functional or timeseries data written by toblerone v{__version__}",
            "AnatomicalStructurePrimary": (
                "CortexLeft" if self.name[0] == "L" else "CortexRight"
            ),
        }

        gii = nibabel.gifti.GiftiImage(meta=nibabel.gifti.GiftiMetaData.from_dict(meta))
        data = data.astype(np.float32)
        d = nibabel.gifti.GiftiDataArray(
            data,
            intent="NIFTI_INTENT_NORMAL",
            datatype="NIFTI_TYPE_FLOAT32",
        )
        gii.add_gifti_data_array(d)

        return gii

    def save_metric(self, data, path):
        """
        Save vertex-wise data as a .func.gii at path
        """

        gii = self.to_metric(data)
        if not path.endswith(".func.gii"):
            path += ".func.gii"
        nibabel.save(gii, path)

    def save(self, path):
        """
        Save surface as .surf.gii (default), .white/.pial at path.
        """
        from .._version import __version__

        if path.endswith(".vtk"):
            # Faces must be an array of polygons with 3 in first
            # columns to denote triangle data
            faces = 3 * np.ones((self.tris.shape[0], 4), dtype=int)
            faces[:, 1:] = self.tris
            m = pyvista.PolyData(self.points, faces)
            m.save(path)

        elif path.count(".gii"):
            if not path.endswith(".surf.gii"):
                if path.endswith(".gii"):
                    path.replace(".gii", ".surf.gii")
                else:
                    path += ".surf.gii"

            sd = self.name[0].upper()
            typ = self.name[1].upper()
            base_meta = {
                "UserName": getpass.getuser(),
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Description": f"Surface geometry data written by toblerone v{__version__}",
            }

            point_meta = {
                "AnatomicalStructurePrimary": (
                    "CortexLeft" if sd == "L" else "CortexRight"
                )
            }
            if typ == "W":
                point_meta["AnatomicalStructureSecondary"] = "GrayWhite"
            elif typ == "P":
                point_meta["AnatomicalStructureSecondary"] = "Pial"
            if typ == "S":
                point_meta["GeometricType"] = "Spherical"
            else:
                point_meta["GeometricType"] = "Anatomical"

            tri_meta = {"TopologicalType": "Closed"}

            # Points matrix
            # 1 corresponds to NIFTI_XFORM_SCANNER_ANAT
            ps = nibabel.gifti.GiftiDataArray(
                self.points,
                intent="NIFTI_INTENT_POINTSET",
                coordsys=nibabel.gifti.GiftiCoordSystem(1, 1),
                datatype="NIFTI_TYPE_FLOAT32",
                meta=nibabel.gifti.GiftiMetaData.from_dict({**base_meta, **point_meta}),
            )

            # Triangles matrix
            ts = nibabel.gifti.GiftiDataArray(
                self.tris,
                intent="NIFTI_INTENT_TRIANGLE",
                coordsys=nibabel.gifti.GiftiCoordSystem(0, 0),
                datatype="NIFTI_TYPE_INT32",
                meta=nibabel.gifti.GiftiMetaData.from_dict({**base_meta, **tri_meta}),
            )

            img = nibabel.gifti.GiftiImage(darrays=[ps, ts])
            nibabel.save(img, path)

        else:
            if not (path.endswith(".white") or path.endswith(".pial")):
                warnings.warn("Saving as FreeSurfer binary")
            nibabel.freesurfer.write_geometry(path, self.points, self.tris)

    def points_within_space(self, spc):
        if not isinstance(spc, rt.ImageSpace):
            spc = rt.ImageSpace(spc)
        ps_vox = self.transform(spc.world2vox).points
        ps_vox = ps_vox.round()
        return np.logical_and((ps_vox > 0).all(-1), (ps_vox <= spc.size - 1).all(-1))

    def transform(self, transform):
        """Apply affine transformation to surface vertices, return new Surface"""

        if isinstance(transform, rt.Registration):
            transform = transform.src2ref
        points = utils.affine_transform(self.points, transform).astype(NP_FLOAT)
        return Surface.manual(points, self.tris, self.name)

    def to_polydata(self):
        """Return pyvista polydata object for this surface"""

        tris = 3 * np.ones((self.tris.shape[0], self.tris.shape[1] + 1), NP_INT)
        tris[:, 1:] = self.tris
        return pyvista.PolyData(self.points, tris)

    def adjacency_matrix(self):
        """
        Adjacency matrix for the points of this surface, as a scipy sparse
        matrix of size P x P, with 1 denoting a shared edge between points.

        """

        edge_pairs = np.array(
            [
                np.concatenate((self.tris[:, 0], self.tris[:, 1], self.tris[:, 2])),
                np.concatenate((self.tris[:, 1], self.tris[:, 2], self.tris[:, 0])),
            ]
        )
        row, col = edge_pairs
        weights = np.ones(row.size, dtype=NP_INT)
        adj = sparse.coo_matrix(
            (weights, (row, col)), shape=(self.n_points, self.n_points)
        )

        return adj.tocsr()

    def mesh_laplacian(self):
        """
        Mesh Laplacian operator for this surface, as a scipy sparse matrix
        of size n_points x n_points. Elements on the diagonal are negative
        and off-diagonal elements are positive. All neighbours are weighted
        with value 1 (ie, equal weighting ignoring distance).

        Returns:
            sparse CSR matrix
        """

        # The diagonal is the negative sum of other elements
        adj = self.adjacency_matrix()
        adj = np.around(
            adj, 9
        )  # FIXME: this is less than ideal - would be better to round to s.f.
        dia = adj.sum(1).A.flatten()
        laplacian = sparse.dia_matrix((dia, 0), shape=(adj.shape), dtype=np.float32)
        laplacian = adj - laplacian

        assert utils.laplacian_is_valid(laplacian)
        return laplacian

    def edges(self):
        """
        Edge matrix, sized as follows (tris, 3, 3), where the second dimension
        contains the edges defined as (v1 - v0), (v2 - v0), (v2 - v1), and
        the final dimension contains the edge components in XYZ.
        """
        edge_defns = [list(e) for e in core.TRI_EDGE_INDEXING]
        edges = np.stack(
            [
                self.points[self.tris[:, e[0]], :] - self.points[self.tris[:, e[1]], :]
                for e in edge_defns
            ],
            axis=1,
        )

        return edges

    def resample_geometry(self, curr_sphere, n_verts=None, new_sphere=None):
        """
        Resample geometry to a different vertex resolution, either to a target
        number of vertices or onto an existing sphere

        Args:
            curr_sphere (Surface): sphere defining current resolution
            n_verts (int): target vertex resolution
            new_sphere (Surface): sphere defining output resolution

        Returns:
            (Surface, Surface) tuple of new surface and new resolution sphere
        """

        if new_sphere is not None:
            if not isinstance(new_sphere, Surface):
                raise ValueError("new_sphere must be a Surface object")
        elif n_verts is None:
            raise ValueError("Must provide either n_verts or new_sphere")
        else:
            new_sphere = Surface.manual(
                *icosphere.icosphere(nr_verts=int(n_verts)), name=curr_sphere.name
            )

        if curr_sphere.n_points != self.n_points:
            raise ValueError(
                "Current sphere must have same number of vertices as surface"
            )

        weights, nearest = utils.barycentric_weights(curr_sphere, new_sphere)

        # Now we can re-use the same weights to interpolate
        # the white and pial surfaces. The new triangles are defined
        # by the output sphere
        new = Surface.manual(
            utils.resample_coordinates(self.points, curr_sphere.tris[nearest], weights),
            new_sphere.tris,
            name=self.name,
        )

        return new, new_sphere


class Hemisphere(object):
    """
    The white and pial surfaces of a hemisphere, and a repository to
    store data when calculating tissue PVs from the fractions of each
    surface

    Args:
        inpath: path to white surface
        outpath: path to pial surface
        side: 'L' or 'R'
    """

    def __init__(self, insurf, outsurf, sphere, side):
        if side not in ["L", "R"]:
            raise ValueError("Side must be either 'L' or 'R'")
        self.side = side.upper()

        # Create surfaces from path or make our own copy
        if not isinstance(insurf, Surface):
            self.inSurf = Surface(insurf, name=self.side + "WS")
        else:
            self.inSurf = copy.deepcopy(insurf)
        if not isinstance(outsurf, Surface):
            self.outSurf = Surface(outsurf, name=self.side + "PS")
        else:
            self.outSurf = copy.deepcopy(outsurf)

        if not isinstance(sphere, Surface):
            self.sphere = Surface(sphere, name=self.side + "SS", shift_cras=False)
            utils.check_spherical(self.sphere.points)
        else:
            self.sphere = copy.deepcopy(sphere)

        if (self.inSurf.tris != self.outSurf.tris).any() or (
            self.inSurf.tris != self.sphere.tris
        ).any():
            raise ValueError("All surfaces must have same triangles array")

        self.PVs = None
        return

    @property
    def surfs(self):
        """Iterator over the inner/outer surfaces, not including sphere"""

        return [self.inSurf, self.outSurf]

    @property
    def surf_dict(self):
        """Return surfs as dict with appropriate keys (eg LPS)"""

        keys = [self.side + n for n in ["WS", "SS", "PS"]]
        vals = [self.inSurf, self.sphere, self.outSurf]
        return dict(zip(keys, vals))

    def transform(self, mat):
        """
        Apply affine transformation to each surface. Returns a new Hemisphre.
        """

        surfs = [s.transform(mat) for s in self.surfs]
        return Hemisphere(*surfs, self.sphere, side=self.side)

    def midsurface(self):
        """Midsurface between inner and outer cortex"""

        vec = self.outSurf.points - self.inSurf.points
        points = self.inSurf.points + (0.5 * vec)
        return Surface.manual(points, self.inSurf.tris, name=f"{self.side}MS")

    def thickness(self):
        vec = self.outSurf.points - self.inSurf.points
        return np.linalg.norm(vec, ord=2, axis=-1)

    def adjacency_matrix(self):
        """
        Adjacency matrix of any cortical surface (they necessarily share
        the same triagulation, which is checked during initialisation).

        """

        return self.inSurf.adjacency_matrix()

    @property
    def n_points(self):
        """Number of vertices on either cortical surface"""
        return self.inSurf.n_points

    def mesh_laplacian(self):
        """
        Mesh Laplacian on cortical midsurface.

        Returns:
            sparse CSR matrix
        """

        return self.midsurface().mesh_laplacian()

    def resample_geometry(self, n_verts=None, new_sphere=None):
        """
        Resample geometry to a different vertex resolution, either
        to a target number of vertices or onto an existing sphere

        Args:
            n_verts (int): target vertex resolution
            new_sphere (Surface): sphere defining output resolution

        Hemisphere object
        """

        (white, pial), new_sphere = utils.resample_surfaces(
            [self.inSurf, self.outSurf],
            self.sphere,
            n_verts=n_verts,
            new_sphere=new_sphere,
        )

        return Hemisphere(white, pial, new_sphere, side=self.side)
