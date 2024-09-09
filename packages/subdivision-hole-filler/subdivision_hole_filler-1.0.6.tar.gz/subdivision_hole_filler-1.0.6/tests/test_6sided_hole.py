import os
import pytest


class Test6SidedHole:
    def test_6sided_hole(self):
        import numpy as np

        from subdivision_hole_filler import Boundary, NsidedHoleFiller

        r = 1
        R = 1

        boundaries = [None, None, None, None, None, None]
        for d in range(3):
            def coord(u: float, d=d):
                phi = (1.0 - u / 2.0) * np.pi / 2.0
                x = r * np.cos(phi)
                y = r * np.sin(phi)
                z = r + R
                c = np.zeros(3)
                c[d] = z
                c[(d + 1) % 3] = x
                c[(d + 2) % 3] = y
                return c

            def deriv(u: float, d=d):
                vec = np.zeros(3)
                vec[d] = -1
                return np.array(vec)

            bd = Boundary()
            bd.coord = coord # A function of parametric coord `u` in [0.0, 2.0], which defines the coordinate of a point on the boundary 
            bd.deriv = deriv # A function of parametric coord `u` in [0.0, 2.0], which defines the cross boundary derivative of a point on the boundary, poining to the inside
            boundaries[d*2] = bd

        for d in range(3):
            def coord(u: float, d=d):
                phi = (1.0 - u / 2.0) * np.pi / 2.0
                x = R + r - R * np.cos(phi)
                y = R + r - R * np.sin(phi)
                z = 0
                c = np.zeros(3)
                c[d] = z
                c[(d + 1) % 3] = x
                c[(d + 2) % 3] = y
                return c
            
            def deriv(u: float, d=d):
                vec = np.zeros(3)
                vec[d] = 1
                return np.array(vec)

            bd = Boundary()
            bd.coord = coord # A function of parametric coord `u` in [0.0, 2.0], which defines the coordinate of a point on the boundary 
            bd.deriv = deriv # A function of parametric coord `u` in [0.0, 2.0], which defines the cross boundary derivative of a point on the boundary, poining to the inside
            boundaries[(d + 1) % 3 * 2 + 1] = bd

        filler = NsidedHoleFiller(boundaries)

        center_point = np.array([r, r, r])
        filler.gen_initial_mesh(center_point)

        for iteration in range(3):
            filler.cmc_subdiv_for_1step(iteration=iteration)


if __name__ == "__main__":
    pytest.main(["-s", "-k", "Test6SidedHole"])