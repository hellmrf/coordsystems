# CoordSystems

CoordSystems is a Python package to help working with different coordinate reference systems at the same time. The intention is to support annotated types for Cartesian, Polar and Spherical coordinates.

## Installation

Just install it with `pip`:
```shell
pip install coordsystems
```

## Usage

The Coordinate types carries out the conversion when needed. For example, when summing a `Cartesian` and a `Spherical`, the `Spherical` will be first converted to `Cartesian`, and then summed up.

```python
from coordsystems import Cartesian, Spherical

c = Cartesian([1, 2, 3]) # x = 1, y = 2, z = 3
s = Spherical([1, 0, 0]) # r = 1, θ = 0, φ = 0
Cartesian(s) # Cartesian([0, 0, 1])
c + s # Cartesian([1, 2, 4])
c.x # 1
s.phi # 0
```

## Cartesian system
In a Cartesian System (here assuming 3D), each coordinate is written as a multiple of a unit basis vector ($\vec i$, $\vec j$ and $\vec k$). Those unit vectors are in the direction usually known as $x$ (for $\vec i$), $y$ (for $\vec j$) and $z$ (for $\vec k$).

To mark a point as a Cartesian point, just use the `Cartesian` constructor, passing a `list` or `numpy.ndarray` with each coordinate, or another `Coordinate` object.

In a Cartesian system, the vector sum is just the element-wise sum. So $(1,2,3) + (1,0,0) = (2,2,3)$.

## Spherical system
In a Spherical System (necessarily 3D), each point is described also by three coordinates (because they are the same $\mathbb{R}^3$ space), but now with $r$ (radius), $\theta$ (polar angle) and $\phi$ (azimuthal angle).

![https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/3D_Spherical.svg/1280px-3D_Spherical.svg.png](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/3D_Spherical.svg/1280px-3D_Spherical.svg.png)

Different from Cartesian systems, here the vector sum isn't trivial. For example, $(2, \frac{\pi}{2}, \pi) + (\frac{1}{2}, \frac{\pi}{6}, 0) = (1.7321, \frac{\pi}{3}, \pi)$. Actually, it's easier to convert them to Cartesian, perform the sum, and convert it back again. Luckily, a `Spherical` object do it for you:

```python
>>> import numpy as np
>>> from coordsystems import Spherical
>>> Spherical([2, np.pi/2, np.pi]) + Spherical([1, np.pi/6, 0])
Spherical([1.7320508075688772, 1.0471975511965976, 3.141592653589793])
```

## Accessing coordinates

In a `p = Cartesian(...)`, you can access directly each coordinate (`p.x`, `p.y`, `p.z`) or use indexing (`p[0] == p['x'] == p.x`).

In a `q = Spherical(...)`, you can also access each coordinate independently (`q.r`, `q.theta` and `q.phi`). Indexing notation isn't implemented yet.

In any case, the implemented operations takes care of the system and try to do any operation in a Cartesian base, converting stuff when appropriate.

## Development

To help in the development of this project, just clone the repository and install the [`uv`](https://docs.astral.sh/uv/) tool as a global dependency (you don't need a global Python executable or a environment manager like `conda` or `pipenv`).

After cloning, you can run the GUI with:

```shell
$ uv run gui
```

It'll create an environment in `.venv/`, install dependencies and run the project inside the correct environment.

## TODO

We still need to implement many things in this package before it gets ready for production.

- [ ] `Number * Coordinate` multiplication
- [ ] `Spherical` indexing access
- [ ] Option to choose the symbol for polar and azimuthal angles (if θ = polar and φ = azimuthal or the opposite).
- [ ] Cartesian custom basis (allow not only the canonical basis).