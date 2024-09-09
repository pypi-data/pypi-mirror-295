# Filler for N-sided holes
[![GitHub release (with filter)](https://img.shields.io/github/v/release/huang-lihao/subdivision-hole-filler?logo=github)
](https://github.com/huang-lihao/subdivision-hole-filler)
[![Upload Python Package](https://github.com/huang-lihao/subdivision-hole-filler/actions/workflows/python-publish.yml/badge.svg)](https://github.com/huang-lihao/subdivision-hole-filler/actions/workflows/python-publish.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/subdivision-hole-filler?logo=pypi)](https://pypi.org/project/subdivision-hole-filler/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/subdivision-hole-filler?logo=PyPI)](https://pypi.org/project/subdivision-hole-filler/)
[![GitHub License](https://img.shields.io/github/license/huang-lihao/subdivision-hole-filler)](https://github.com/huang-lihao/subdivision-hole-filler/blob/main/LICENSE)


A python package to fill N-sided holes using combined subdivision schemes, based on Catmull-Clark subdivison.

See [Levin, Adi. “Filling N-sided Holes Using Combined Subdivision Schemes.” (2000).](https://github.com/huang-lihao/subdivision-hole-filler/blob/main/Levin_2000_Filling%20N-sided%20Holes%20Using%20Combined%20Subdivision%20Schemes.pdf)


Install
----------------------
Use PyPI to install [subdivision-hole-filler](https://pypi.org/project/subdivision-hole-filler/):
```sh
pip install subdivision-hole-filler
```

Usage
----------------------
Run the following script to fill a hole.
```python
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

```

Here is the ouput.

<center class="half">
    <img src="https://github.com/huang-lihao/subdivision-hole-filler/raw/main/iso.png" width="45%"/><img src="https://github.com/huang-lihao/subdivision-hole-filler/raw/main/side.png" width="45%"/>
</center>
