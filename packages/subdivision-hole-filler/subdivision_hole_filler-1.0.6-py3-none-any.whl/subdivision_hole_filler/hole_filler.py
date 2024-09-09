"""

See Levin 1999 paper: "Filling an N-sided hole using combined subdivision schemes
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import numpy as np
from scipy.interpolate import PPoly


catmull_clark_coefs = {}

def get_catmull_clark_coef(m):
    if m in catmull_clark_coefs:
        return catmull_clark_coefs[m]
    k = np.cos(np.pi / m)
    pp = PPoly(np.array([[1, 0, 4 * k ** 2 - 3, - 2 * k]]).T, [0, 10])
    x = pp.roots()[0]
    W = x ** 2 + 2 * k * x - 3
    alpha = 1
    gamma = (k * x + 2 * k ** 2 - 1)/(x**2*(k*x + 1))
    beta = - gamma
    catmull_clark_coefs[m] = (W, alpha, beta, gamma)
    return catmull_clark_coefs[m]


class Boundary:
    def __init__(self):
        pass

    def coord(self, u: float):
        raise NotImplementedError

    def deriv(self, u: float):
        raise NotImplementedError


class Point:
    def __init__(self, x, y, z, boundary_u_tuples: list[tuple[Boundary, float]] = []):
        self.coord = np.array([x, y, z])
        self.boundary_u_tuples = boundary_u_tuples
        assert len(boundary_u_tuples) in [0, 1, 2]
        self.neighbours: list[Point] = []
        self.faces: list[Face] = []
        self.id = -1

        self.parametric_coord_in_sub_face: dict[int, np.ndarray] = {}


class Face:
    def __init__(self, points: list[Point], sub_face: int) -> None:
        assert len(points) == 4
        self.points = points
        for i in range(4):
            points[i].faces.append(self)
            for d in [-1, +1]:
                j = (i + d) % 4
                if points[j] not in points[i].neighbours:
                    points[i].neighbours.append(points[j])
        self.sub_face = sub_face
        
    
    def center_point(self) -> Point:
        point = Point(*np.mean([p.coord for p in self.points], axis=0))
        point.parametric_coord_in_sub_face[self.sub_face] = 0.25 * (
            self.points[0].parametric_coord_in_sub_face[self.sub_face] +
            self.points[1].parametric_coord_in_sub_face[self.sub_face] +
            self.points[2].parametric_coord_in_sub_face[self.sub_face] +
            self.points[3].parametric_coord_in_sub_face[self.sub_face]
        )
        return point


def get_edge_tuple(point1: Point, point2: Point, points: list[Point]) -> tuple[Point, Point]:
    idxi = points.index(point1)
    idxj = points.index(point2)
    idx1, idx2 = sorted([idxi, idxj])
    return (points[idx1], points[idx2])


class NsidedHoleFiller:
    def __init__(self, boundaries: list[Boundary]) -> None:
        self.boundaries = boundaries
        self.points: list[Point] = []
        self.faces: list[Face] = []
        self.iteration = 0
    
    def plot_faces(self, output_path: str = None, boundary_colors: list[str] = None, facecolor: str = "none", show_quiver: bool = True):
        faces = self.faces
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        fig.set_size_inches(3, 3)
        for face in faces:
            coord = [pt.coord for pt in face.points]
            coord = np.array([[coord[0], coord[1]], [coord[3], coord[2]]])
            X = coord[:, :, 0]
            Y = coord[:, :, 1]
            Z = coord[:, :, 2]
            ax.plot_surface(X,Y,Z,color=facecolor, edgecolor="black", zsort="max", zorder=0)
        ax.plot([self.center_point.coord[0]], [self.center_point.coord[1]], [self.center_point.coord[2]], "o", color="darkgreen", zorder=1e10)

        if boundary_colors is None:
            boundary_colors = [f"C{i}" for i in range(len(self.boundaries))]
        for idx, bd in enumerate(self.boundaries):
            coord = np.array([bd.coord(u) for u in np.linspace(0, 2, 101, endpoint=True)])
            deriv = np.array([bd.deriv(u) for u in np.linspace(0, 2, 101, endpoint=True)])
            color = boundary_colors[idx]
            ax.plot(coord[:, 0], coord[:, 1], coord[:, 2], color=color, zorder=1e10)
            indices = np.linspace(0, 100, 5, endpoint=True).astype(int)
            if show_quiver:
                ax.quiver(
                    coord[indices, 0], coord[indices, 1], coord[indices, 2], deriv[indices, 0], deriv[indices, 1], deriv[indices, 2],
                    length=1, normalize=True, color=color, zorder=1e10,pivot="tip"
                )
        plt.axis('equal')
        ax.set_proj_type('ortho')
        ax.view_init(elev=np.arctan(np.sqrt(0.5))/np.pi*180, azim=45)
        ax.axis('off')
        # ax.set_visible(False)
        if output_path is not None:
            plt.tight_layout()
            plt.savefig(output_path, dpi=600)
            import pickle
            pickle.dump(fig, open(output_path+".pickle", 'wb'))
        else:
            plt.show()

    def gen_initial_mesh(self, center_point_coord: np.ndarray) -> None:
        r"""
        Generate the initial mesh as in Levin 1999 paper.

        .. code-block:: python

                      *------+------*
                     /       |       \
                    /        |        \
                   +---------o---------+
                  /         / \         \
                 /         /   \         \
                *         /     \         *
                 \       /       \       /
                  \     /         \     /
                   \   /           \   /
                    \ /             \ /
                     x               x
                      \             /
                       \           /
                        \         /
                         \       /
                          \     /
                           \   /
                            \ /
                             *

        Args:
            boundaries (list[Boundary]):
                Boundaries having exact coordinates and tangential direction
            center_point_coord (np.ndarray):
                The center point coordinates to generate the initial mesh
        """
        boundaries = self.boundaries
        num = len(boundaries)

        # check adjacent boundaries are linked together
        for i in range(num):
            j = (i + 1) % num
            b1 = boundaries[i]
            b2 = boundaries[j]
            assert np.allclose(b1.coord(2), b2.coord(0)), f"Adjacent boundaries are not linked together, {b1.coord(2)}, {b2.coord(0)}"
        
        points: list[Point] = []
        faces: list[Face] = []
        for i, boundary in enumerate(boundaries):
            l = (i - 1) % num
            left_boundary = boundaries[l]
            points.append(Point(*boundary.coord(0.0), [(left_boundary, 2.0), (boundary, 0.0)]))
            points.append(Point(*boundary.coord(1.0), [(boundary, 1.0)]))
        points.append(Point(*center_point_coord))
        center_point = points[-1]
        self.center_point = center_point

        for i in range(num):
            vertices = [
                points[2 * i],
                points[(2 * i + 1) % (2* num)],
                center_point,
                points[(2 * i -1) % (2 * num)]
            ]
            vertices[0].parametric_coord_in_sub_face[i] = np.array([0.0, 0.0])
            vertices[1].parametric_coord_in_sub_face[i] = np.array([1.0, 0.0])
            vertices[2].parametric_coord_in_sub_face[i] = np.array([1.0, 1.0])
            vertices[3].parametric_coord_in_sub_face[i] = np.array([0.0, 1.0])
            faces.append(Face(
                points=vertices,
                sub_face=i
            ))
        self.points = points
        self.faces = faces
    
    def clear_points(self, points: list[Point] = None):
        if points is None: points = self.points
        for point in points:
            point.neighbours = []
            point.faces = []

    def cmc_subdiv_for_1step(self, iteration: int) -> None:
        assert iteration == self.iteration
        step = 2**(-iteration)
        points = self.points
        faces = self.faces
        new_faces: list[Face] = []
        new_points: list[Point] = []
        new_points.extend(points)
        for point in points:
            # A smooth boundary rule 0 < u < 2
            if len(point.boundary_u_tuples) == 1:
                boundary, u = point.boundary_u_tuples[0]
                c = boundary.coord
                d = boundary.deriv
                w = [p for p in point.neighbours if len(p.boundary_u_tuples) == 0][0].coord
                point.coord = 2 * c(u) - 1/2 * w - 1/4 * (c(u + step) + c(u - step)) - step/12*(d(u + step) + d(u - step)) + step*2/3*d(u)
            
            # A smooth corner rule u = 0, 2
            if len(point.boundary_u_tuples) == 2:
                boundary1, u1 = point.boundary_u_tuples[0]
                boundary2, u2 = point.boundary_u_tuples[1]
                if np.allclose(u2, 0.0):
                    assert np.allclose(u1, 2.0)
                    c = boundary2.coord
                    cl = boundary1.coord
                    d = boundary2.deriv
                    dl = boundary1.deriv
                elif np.allclose(u1, 0.0):
                    assert np.allclose(u2, 2.0)
                    c = boundary1.coord
                    cl = boundary2.coord
                    d = boundary1.deriv
                    dl = boundary2.deriv
                else:
                    raise ValueError(f"This should not happen, u1 = {u1}, u2 = {u2}")

                assert len(point.faces) == 1
                face = point.faces[0]
                diag = [p for p in face.points if p not in point.neighbours + [point]]
                assert len(diag) == 1
                w = diag[0].coord  
                point.coord = 5/2 * c(0) + 1/4 * w - (c(step) + cl(2 - step)) + 1/8 * (c(2*step) + cl(2 - 2*step)) + step * 29/48 * (d(0) + dl(2)) - step * 1/12 * (d(step) + dl(2 - step)) - step * 1/48 * (d(2*step) + dl(2 - 2*step))

        # Sabin's variation of the Catmull-Clark subdivision rule
        # For each face, add a face point
        face_points: dict[Face, Point] = {}
        for face in faces:
            face_point = face.center_point()
            face_points[face] = face_point
            new_points.append(face_point)
        
        # For each edge, add an edge point
        edge_faces: dict[tuple[Point, Point], list[Face]] = {}
        for face in faces:
            for i in range(4):
                j = (i + 1) % 4
                edge = get_edge_tuple(face.points[i], face.points[j], points)
                if edge not in edge_faces: edge_faces[edge] = []
                edge_faces[edge].append(face)
    
        edge_points = {}
        for edge in edge_faces:
            boundaries1 = [bu[0] for bu in edge[0].boundary_u_tuples]
            boundaries2 = [bu[0] for bu in edge[1].boundary_u_tuples]
            common_boundary = [b for b in boundaries1 if b in boundaries2]
            assert len(common_boundary) in [0, 1]
            boundary_u_tuples = []
            if len(common_boundary) == 1:
                boundary = common_boundary[0]
                u1 = [bu[1] for bu in edge[0].boundary_u_tuples if bu[0] == boundary][0]
                u2 = [bu[1] for bu in edge[1].boundary_u_tuples if bu[0] == boundary][0]
                u = 1/2 * (u1 + u2)
                boundary_u_tuples.append((boundary, u))
            face_centers = [face_points[face].coord for face in edge_faces[edge]]
            ends = [edge[0].coord, edge[1].coord]
            coord = np.mean(face_centers + ends, axis=0)
            edge_point = Point(
                *coord,
                boundary_u_tuples=boundary_u_tuples,
            )
            for face in edge_faces[edge]:
                edge_point.parametric_coord_in_sub_face[face.sub_face] = 0.5 * (
                    edge[0].parametric_coord_in_sub_face[face.sub_face] + edge[1].parametric_coord_in_sub_face[face.sub_face]
                )
            edge_points[edge] = edge_point
            new_points.append(edge_points[edge])
        
        # Move each original point to the new vertex point
        for point in points:
            F = np.mean(
                [face_points[face].coord for face in point.faces],
                axis=0
            )
            E = np.mean(
                [1/2*(point.coord + q.coord) for q in point.neighbours],
                axis=0
            )
            P = point.coord
            m = max(len(point.neighbours), 4)
            W, alpha, beta, gamma = get_catmull_clark_coef(m)
            alpha = 2 * (m - 1) / (3 * m)
            beta = 1 * (m - 1) / (3 * m)
            gamma = 1 / m
            point.coord = alpha * E + beta * F + gamma * P

        # Form faces in the new mesh
        self.clear_points(points)
        for face in faces:
            for i in range(4):
                mid = []
                for d in [-1, +1]:
                    j = (i + d) % 4
                    edge = get_edge_tuple(face.points[i], face.points[j], points)
                    mid.append(edge_points[edge])
                new_faces.append(Face(
                    points = [face.points[i], mid[0], face_points[face], mid[1]],
                    sub_face = face.sub_face
                ))
        
        # sample boundary points
        for point in new_points:
            if len(point.boundary_u_tuples) > 0:
                boundary, u = point.boundary_u_tuples[-1]
                point.coord = boundary.coord(u)

        self.faces = new_faces
        self.points = new_points
        self.iteration += 1
    
    def gen_bspline_surfaces(self) -> list[list[np.ndarray]]:
        bspline_surfaces = []
        num = len(self.boundaries)
        for n in range(num):
            points_in_sub_face = []
            for point in self.points:
                if n not in point.parametric_coord_in_sub_face: continue
                points_in_sub_face.append(point)
                        
            points_in_sub_face = sorted(
                points_in_sub_face,
                key=lambda p: (
                    p.parametric_coord_in_sub_face[n][0],
                    p.parametric_coord_in_sub_face[n][1]
                )
            )
            bspline_surfaces.append(points_in_sub_face)
        return bspline_surfaces