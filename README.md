# CoordSystems

CoordSystems is a Python package to help working with different coordinate reference systems at the same time. The intention is to support annotated types for Cartesian, Polar and Spherical coordinates.

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