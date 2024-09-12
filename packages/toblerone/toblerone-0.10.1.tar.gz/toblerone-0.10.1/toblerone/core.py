# Core numerical functions for Toblerone

# This module contains the key functions that operate on patches of surface (see
# classes module) to estimate the fraction of a voxel enclosed within said patch.
# The most computationally intensive methods are handled by Cython in the module
# ctoblerone (see extern/ctoblerone.pyx). Finally, certain functions that are re-
# used between modules are defined in pvcore.

# This module should not be directly interacted with: the modules estimators and
# pvtools provide outward-facing wrappers for actual PV estimation.

import itertools
from scipy import sparse

import numpy as np
import trimesh
from numba import jit

from toblerone import utils, core
from toblerone.utils import NP_FLOAT, NP_INT


# Module level constants ------------------------------------------------------

# See the _vox_tri_weights_worker() function for an explanation of the
# naming convention here.
TETRA1 = np.array(
    [[0, 3, 4, 5], [0, 1, 2, 4], [0, 2, 4, 5]], dtype=NP_INT  # aABC  # abcB  # acBC
)

TETRA2 = np.array(
    [[0, 3, 4, 5], [0, 1, 2, 5], [0, 1, 4, 5]], dtype=NP_INT  # aABC  # abcC  # abBC
)

# For defining the edges of triangle within a mesh
TRI_EDGE_INDEXING = [{1, 0}, {2, 0}, {2, 1}]
TRI_FULL_SET = set(range(3))

# Functions -------------------------------------------------------------------


@jit
def test_ray_triangles_intersection(tris, vertices, orig, ax1, ax2):
    """
    Test if ray intersects triangles. The ray must be axis-aligned;
    for example if [0 0 1], in which case ax1 and ax2 are 0 and 1.

    Args:
        tris: tx3 array of triangle vertex indices
        vertices: nx3 array of vertex coordinates
        orig: 1x3 array of ray origin
        ax1: int, first axis the ray doesn't travel along
        ax2: int, the other axis the ray doesn't travel along

    Returns:
        tx1 boolean array, true if triangle intersects ray
    """

    result = np.zeros(tris.shape[0], dtype=np.bool_)
    tv = np.zeros((3, 3), dtype=NP_FLOAT)

    for tind in range(tris.shape[0]):
        # tv = vertices[tris[tind], :]
        for i in range(3):
            for j in range(3):
                tv[i, j] = vertices[tris[tind, i], j]

        intersection = False
        j = 2

        # start with the wraparound case
        for i in range(3):
            # if one vertex is on one side of the point in the x direction, and the other is on the other side (equal case is treated as greater)
            if (tv[i, ax1] < orig[ax1]) != (tv[j, ax1] < orig[ax1]):
                # reorient the segment consistently to get a consistent answer
                if tv[i, ax1] < tv[j, ax1]:
                    ti = i
                    tj = j
                else:
                    ti = j
                    tj = i

                # if the point on the line described by the two vertices with the same x coordinate is above (greater y) than the test point
                if (tv[ti, ax2] - tv[tj, ax2]) / (tv[ti, ax1] - tv[tj, ax1]) * (
                    orig[ax1] - tv[tj, ax1]
                ) + tv[tj, ax2] > orig[ax2]:
                    # even/odd winding rule
                    intersection = not intersection

            # consecutive vertices, does 2,0 then 0,1 then 1,2
            j = i

        result[tind] = intersection

    return result


@jit
def _findRayTriangleIntersections3D(testPnt, ray, points, tris, xprods):
    """Find points of intersection between a ray and a surface. Triangles
    are projected down onto a 2D plane normal to the ray. See:
    https://stackoverflow.com/questions/2500499/howto-project-a-planar-polygon-on-a-plane-in-3d-space
    https://stackoverflow.com/questions/11132681/what-is-a-formula-to-get-a-vector-perpendicular-to-another-vector

    Args:
        testPnt: 1 x 3 vector for origin of ray
        ray: 1 x 3 direction vector of ray
        points: n x 3 array of triangle vertices
        tris: m x 3 array of triangle vertex indices
        xprods: m x 3 array of triangle face normals

    Returns:
        1 x j vector of distance multipliers along the ray at each point
        of intersection
    """

    # Intersection is tested using Tim Coalson's adaptation of PNPOLY for careful
    # testing of intersections between infinite rays and points. As TC's adaptation
    # is a 2D test only (with the third dimension being the direction of ray
    # projection), triangles are flattened into 2D before testing. This is done by
    # projecting all triangles onto the plane defined by the ray (acting as planar
    # normal) and then testing for ray intersection (where the ray now represents
    # the Z direction in this new projected space) amongst all the triangles in
    # dimensions 1 and 2 (XY). Define a new coordinate system (d unit vectors)
    # with d3 along the ray, d2 and d1 in plane.
    if np.abs(ray[2]) < np.abs(ray[0]):
        d2 = np.array([ray[1], -ray[0], 0], dtype=NP_FLOAT)
    else:
        d2 = np.array([0, -ray[2], ray[1]], dtype=NP_FLOAT)
    d1 = np.cross(d2, ray)

    # Calculate the projection of each point onto the direction vector of the
    # surface normal. Then subtract this component off each to leave their position
    # on the plane and shift coordinates so the test point is the origin.
    lmbda = np.dot(points, ray)
    onPlane = points - np.outer(lmbda, ray) - testPnt

    # Re-express the points in 2d planar coordiantes by evaluating dot products with the d2 and d3 in-plane orthonormal unit vectors
    onPlane2d = np.vstack(
        (
            np.dot(onPlane, d1),
            np.dot(onPlane, d2),
            np.zeros(lmbda.size, dtype=NP_FLOAT),
        )
    )

    # Now perform the test
    fltr = test_ray_triangles_intersection(
        tris, onPlane2d.T, np.zeros(3, dtype=NP_FLOAT), 0, 1
    )

    # # For those trianglest that passed, calculate multiplier to point of
    # # intersection
    # mu is defined as dot((p_plane - p_test), normal_tri_plane) ...
    #   / dot(ray, normal_tri_plane)
    dotRN = np.dot(xprods[fltr], ray)
    mu = np.sum((points[tris[fltr, 0], :] - testPnt) * xprods[fltr], axis=1)

    return mu / dotRN


def _get_subvoxel_grid(supr):
    """Generate grid of subvoxel centers"""

    steps = 1.0 / supr
    subs = np.indices(supr.astype(int)).reshape(3, -1).T / supr
    subs += (steps / 2) - 0.5

    return subs.astype(NP_FLOAT)


def vox_tri_weights(in_surf, out_surf, spc, factor, ones=False):
    """
    Form matrix of size (n_vox x n_tris), in which element (I,J) is the
    fraction of samples from voxel I that are in triangle prism J.

    Args:
        in_surf: Surface object, inner surface of cortical ribbon
        out_surf: Surface object, outer surface of cortical ribbon
        spc: ImageSpace object within which to project
        factor: voxel subdivision factor

    Returns:
        vox_tri_weights: a scipy.sparse CSR matrix of shape
            (n_voxs, n_tris), in which each entry at index [I,J] gives the
            number of samples from triangle prism J that are in voxel I.
            NB this matrix is not normalised in any way!
    """

    # vertices in voxel coordinates
    in_verts, out_verts = [
        utils.affine_transform(s.points, spc.world2vox) for s in [in_surf, out_surf]
    ]

    # grid of subvoxel centers
    factor = (factor * np.ones(3)).astype(int)
    sub_grid = core._get_subvoxel_grid(factor)

    # sparse matrix to store the weights
    vox_tri_weights = sparse.dok_matrix(
        (spc.size.prod(), in_surf.tris.shape[0]), dtype=NP_FLOAT
    )

    # Loop over each triangle, construct the triangular prism, check for intersection
    for t, tri in enumerate(in_surf.tris):
        # Stack the vertices of the inner and outer triangles into a 6x3 array.
        # We will then refer to these points by the indices abc, ABC; lower
        # case for the white surface, upper for the pial. We also cycle the
        # vertices (note, NOT A SHUFFLE) such that the highest index is first
        # (corresponding to A,a). The relative ordering of vertices remains the
        # same, so we use flagsum to check if B < C or C < B.
        tri_max = np.argmax(tri)
        tri_sort = [tri[(tri_max + i) % 3] for i in range(3)]
        flagsum = sum([int(tri_sort[v] < tri_sort[(v + 1) % 3]) for v in range(3)])

        # Two positive divisions and one negative
        if flagsum == 2:
            tets = TETRA1

        # This MUST be two negatives and one positive.
        else:
            tets = TETRA2

        hull_ps = np.vstack((in_verts[tri_sort, :], out_verts[tri_sort, :]))

        # Get the neighbourhood of voxels through which this prism passes
        # in linear indices (note the +1 otherwise np.indices doesn't return
        # any voxels for size=1 in a dimension)
        bbox = np.vstack((hull_ps.min(0), hull_ps.max(0))).round()
        bbox = np.clip(bbox, 0, spc.size - 1).astype(int)
        hood = np.indices(bbox[1, :] - bbox[0, :] + 1).reshape(3, -1).T + bbox[0, :]

        # The bbox may not intersect any voxels within the FoV at all, skip
        if not hood.size:
            continue

        hood_vidx = np.ravel_multi_index(hood.T, spc.size)

        # Debug mode: just stick ones in all candidate voxels and continue
        if ones:
            vox_tri_weights[hood_vidx, t] = sub_grid.shape[0]
            continue

        for vidx, ijk in zip(hood_vidx, hood.astype(NP_FLOAT)):
            v_samps = ijk + sub_grid

            # The two triangles form an almost triangular prism in space (like a
            # toblerone bar...). It has 6 vertices and 8 triangular faces (2 end
            # caps, 3 almost rectangular side faces that are further split into 2
            # triangles each). Splitting the quadrilateral faces into triangles is
            # the tricky bit as it can be done in two ways, as below.
            #
            #   pial
            # N______N+1
            #  |\  /|
            #  | \/ |
            #  | /\ |
            # n|/__\|n+1
            #   white
            #
            # It is important to ensure that neighbouring prisms share the same
            # subdivision of their adjacent faces (ie, both of them agree to split
            # it in the \ or / direction) to avoid double counting regions of space.
            # This is achieved by enumerating the triangular faces of the prism in
            # a specific order according to the index numbers of the triangle
            # vertices. For each vertex n, if the index number of vertex n+1 (with
            # wraparound for the last vertex) is greater, then we split the face
            # that the edge (n, n+1) belongs to in a "positive" manner. Otherwise,
            # we split the face in a "negative" manner. A positive split means that
            # a diagonal will go from the pial vertex N to white vertex n+1. A
            # negative split will go from pial vertex N+1 to white vertex n. As a
            # result, around the complete prism formed by the two triangles, there
            # will be two face diagonals that ALWAYS meet at the WHITE vertex
            # with the HIGHEST index number (referred to as 'a'). With these two
            # diagonals fixed, the order of the last diagonal depends on the
            # condition B < C (+ve) or C < B (-ve). We check this using the
            # flagsum variable, which will be 2 for B < C or 1 for C < B. Finally,
            # knowing how the last diagonal is arranged, there are exactly two
            # ways of splitting the prism down, hardcoded at the top of this file.
            # See http://www.alecjacobson.com/weblog/?p=1888.

            # Test the sample points against the tetrahedra. We don't care about
            # double counting within the polyhedra (although in theory this
            # shouldn't happen). Hull formation can fail due to geometric
            # degeneracy so wrap it up in a try block
            samps_in = np.zeros(v_samps.shape[0], dtype=bool)
            for tet in tets:
                samps_in |= test_points_in_tetra(v_samps, hull_ps[tet, :])

            # Don't write explicit zero
            if samps_in.any():
                vox_tri_weights[vidx, t] = samps_in.sum()

    return vox_tri_weights.tocsr()


@jit
def test_points_in_tetra(point, tetra_verts):
    """
    Test if nx3 array of points are contained in the tetrahedron defined by 4x3 array tetra_verts.

    Returns:
        nx1 boolean array, true if point is in tetrahedron
    """

    origin = tetra_verts[0]
    mat = (tetra_verts[1:] - origin).T
    try:
        tetra = np.linalg.inv(mat)
    except Exception:
        return np.zeros(point.shape[0], dtype=np.bool_)

    newp = (tetra @ (point - origin).T).T
    return ((newp >= 0).sum(1) == 3) & ((newp <= 1).sum(1) == 3) & (newp.sum(1) <= 1)


def vtx_tri_weights(surf):
    """
    Form a matrix of size (n_vertices x n_tris) where element (I,J) corresponds
    to the area of triangle J belonging to vertex I.

    Areas are calculated according to the definition of A_mixed in "Discrete
    Differential-Geometry Operators for Triangulated 2-Manifolds", M. Meyer,
    M. Desbrun, P. Schroder, A.H. Barr.

    With thanks to Jack Toner for the original code from which this is adapted.

    Args:
        surf: Surface object

    Returns:
        sparse CSR matrix, size (n_points, n_tris) where element I,J is the
            area of triangle J belonging to vertx I
    """

    points = surf.points
    tris = surf.tris
    edges = np.stack(
        (
            points[tris[:, 1], :] - points[tris[:, 0], :],
            points[tris[:, 2], :] - points[tris[:, 0], :],
            points[tris[:, 2], :] - points[tris[:, 1], :],
        ),
        axis=1,
    )
    edge_lengths = np.linalg.norm(edges, axis=2)

    # We pre-compute all triangle edges, in the following order:
    # e1-0, then e2-0, then e2-1. But we don't necessarily process
    # the edge lengths in this order, so we need to keep track of them
    result = sparse.dok_matrix((points.shape[0], tris.shape[0]), dtype=NP_FLOAT)

    # Iterate through each triangle containing each point
    for pidx in range(points.shape[0]):
        tris_touched = tris == pidx

        for tidx in np.flatnonzero(tris_touched.any(-1)):
            # We need to work out at which index within the triangle
            # this point sits: could be {0,1,2}, call it the cent_pidx
            # Edge pairs e1 and e2 are defined as including cent_pidx (order
            # irrelevant), then e3 is the remaining edge pair
            cent_pidx = np.flatnonzero(tris_touched[tidx]).tolist()
            e3 = TRI_FULL_SET.difference(cent_pidx)
            other_idx = list(e3)
            e1 = set(cent_pidx + [other_idx[0]])
            e2 = set(cent_pidx + [other_idx[1]])

            # Match the edge pairs to the order in which edges were calculated
            # earlier
            e1_idx, e2_idx, e3_idx = [
                np.flatnonzero([e == ei for ei in TRI_EDGE_INDEXING])
                for e in [e1, e2, e3]
            ]

            # And finally load the edges in the correct order
            L12 = edge_lengths[tidx, e3_idx]
            L01 = edge_lengths[tidx, e1_idx]
            L02 = edge_lengths[tidx, e2_idx]

            # Angles
            alpha = np.arccos(
                (np.square(L01) + np.square(L02) - np.square(L12)) / (2 * L01 * L02)
            )
            beta = np.arccos(
                (np.square(L01) + np.square(L12) - np.square(L02)) / (2 * L01 * L12)
            )
            gamma = np.arccos(
                (np.square(L02) + np.square(L12) - np.square(L01)) / (2 * L02 * L12)
            )
            angles = np.array([alpha, beta, gamma])

            # Area if not obtuse
            if not (angles > np.pi / 2).any():  # Voronoi
                a = (
                    (np.square(L01) / np.tan(gamma)) + (np.square(L02) / np.tan(beta))
                ) / 8
            else:
                # If obtuse, heuristic approach
                area_t = 0.5 * np.linalg.norm(
                    np.cross(edges[tidx, 0, :], edges[tidx, 1, :])
                )
                if alpha > np.pi / 2:
                    a = area_t / 2
                else:
                    a = area_t / 4

            result[pidx, tidx] = a

    result = result.tocsr()
    assert (result.data > 0).all(), "Zero areas returned"

    return result


def binary_voxelise(mesh_in_vox, space):
    """
    Binary voxelise (in/out) a triangular mesh within its minimal bounding box

    Args:
        mesh_in_vox: trimesh object of the mesh already in voxel coordinates

    Returns:
        (np.ndarray) binary 3D array of the mesh, true if inside the mesh
    """

    lb = np.floor(mesh_in_vox.vertices.min(0)).astype(int)
    vertices = (mesh_in_vox.vertices - lb).astype(NP_FLOAT)
    sz = np.ceil(vertices.max(0)).astype(int)
    mesh = trimesh.Trimesh(vertices, mesh_in_vox.faces)
    mask = np.zeros(sz, dtype=bool)

    dim = 2
    start_point = np.array([0, 0, -1.0], dtype=NP_FLOAT)
    ray = np.array([0, 0, 1.0], dtype=NP_FLOAT)
    indices = np.arange(sz[dim], dtype=int)

    for x, y in itertools.product(range(sz[0]), range(sz[1])):
        bounds = np.array(
            [
                x - 0.5,
                y - 0.5,
                -0.5,
                x + 0.5,
                y + 0.5,
                sz[dim] + 0.5,
            ]
        )
        local_tris = list(mesh.triangles_tree.intersection(bounds))
        if not local_tris:
            continue

        submesh = mesh.submesh(
            [local_tris], append=True, repair=False, only_watertight=False
        )
        start_point[[0, 1]] = x, y

        int_norm = _findRayTriangleIntersections3D(
            start_point, ray, submesh.vertices, submesh.faces, submesh.face_normals
        )

        assert not (
            int_norm.size % 2
        ), "should be even number of intersections for closed surface"

        # Calculate points of intersection along the ray.
        int_norm = np.sort(int_norm) - 1

        # Assignment. All voxels before the first point of intersection
        # are outside. The mask is already zeroed for these. All voxels
        # between point 1 and n could be in or out depending on parity
        for i in range(1, len(int_norm) + 1):
            # Starting from infinity, all points between an odd numbered
            # intersection and the next even one are inside the mask
            # Points beyond the last intersection are outside the mask
            if (i % 2) & ((i + 1) <= len(int_norm)):
                fltr = (indices > int_norm[i - 1]) & (indices < int_norm[i])
                mask[x, y, indices[fltr]] = 1

    # which voxels did we touch, and are they in the output space?
    out = np.zeros(space.size, dtype=bool)
    vox_ijk = np.indices(mask.shape).reshape(3, -1).T
    vox_ijk_out = vox_ijk + lb
    valid = (vox_ijk_out >= 0).all(-1) & (vox_ijk_out < space.size).all(-1)
    out[*vox_ijk_out[valid].T] = mask[*vox_ijk[valid].T]

    return out


@jit
def fractional_voxelise(
    vertices_list,
    faces_list,
    normals_list,
    vox_cent,
    sub_grid,
):
    sub_fraction = 1 / sub_grid.shape[0]
    fractions = np.zeros(vox_cent.shape[0], dtype=NP_FLOAT)

    for idx, (ijk, vs, ts, ns) in enumerate(
        zip(vox_cent, vertices_list, faces_list, normals_list)
    ):
        inside = 0.0
        for tp, dv in zip(sub_grid + ijk, -sub_grid):
            int_norm = _findRayTriangleIntersections3D(tp, dv, vs, ts, ns)

            # even number of intersections in [0,1] means point is inside
            in_range = (int_norm > 0) & (int_norm < 1)
            if not (in_range.sum() % 2):
                inside += sub_fraction

        fractions[idx] = inside

    return fractions


def voxelise(surface, space, factor=None, binary=False):
    """
    Voxelise a surface within an ImageSpace, potentially returning
    partial volume fractions. Only the fraction of surface intersecting
    the voxel grid will be considered.

    Args:
        surface (Surface): triangular surface in world-mm coordinates
        space (ImageSpace): ImageSpace object within which to operate
        factor (np.ndarray): supersampling factor (3-vector) to use for estimation
        binary (bool): whole-voxel assignment only, don't consider PVs

    Returns:
        np.ndarray: 3D array of partial volume float fractions
    """

    if factor is None:
        factor = 2 * np.ceil(space.vox_size)
    factor = (factor * np.ones(3)).astype(int)

    # Convert surface into voxel coordinates and create a trimesh object
    surf_in_vox = surface.transform(space.world2vox)
    mesh = trimesh.Trimesh(surf_in_vox.points, surface.tris, validate=True)

    voxelised = binary_voxelise(mesh, space)
    pvs = voxelised.flatten().astype(NP_FLOAT)

    if binary:
        return pvs

    # TODO this logic for getting full FoV is duplicated in binary_voxelise
    lb = np.maximum(0, np.floor(mesh.vertices.min(0))).astype(int)
    ub = np.minimum(space.size - 1, np.ceil(mesh.vertices.max(0))).astype(int)
    sz = ub - lb
    to_process = np.indices(sz + 1).reshape(3, -1).T + lb
    fltr = (to_process >= 0).all(1) & (to_process < space.size).all(1)
    to_process = to_process[fltr]
    to_process_bnds = np.concatenate((to_process - 0.5, to_process + 0.5), axis=1)
    tri_int = [list(mesh.triangles_tree.intersection(b)) for b in to_process_bnds]
    fltr = [bool(t) for t in tri_int]
    to_process = to_process[fltr, :]
    submeshes = mesh.submesh(tri_int, append=False, repair=False, only_watertight=False)

    valid = (to_process >= 0).all(-1) & (to_process < space.size).all(-1)
    to_process = to_process[valid, :]
    to_process_inds = np.ravel_multi_index(to_process.T, space.size)
    to_process = to_process.astype(NP_FLOAT)

    sub_grid = _get_subvoxel_grid(factor)
    vertices_list = [sm.vertices for sm in submeshes]
    faces_list = [sm.faces for sm in submeshes]
    normals_list = [sm.face_normals for sm in submeshes]

    fractions = fractional_voxelise(
        vertices_list, faces_list, normals_list, to_process, sub_grid
    )

    to_invert = ~voxelised.flat[to_process_inds]
    fractions[to_invert] = 1 - fractions[to_invert]
    pvs[to_process_inds] = fractions

    return np.clip(pvs, 0, 1).reshape(space.size)
