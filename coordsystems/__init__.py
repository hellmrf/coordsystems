from abc import ABC
from numbers import Number
from typing import Optional, Union

import numpy as np
from plum import dispatch


class Coordinate(ABC):
    pass


class Cartesian(Coordinate):
    point: np.ndarray

    @dispatch
    def __init__(self, point: Union[list, np.ndarray]):
        self.point = np.array(point)

    @dispatch
    def __init__(self, point: "Cartesian"):
        self.point = point.point

    @dispatch
    def __init__(self, p: "Spherical"):
        x = p.r * np.sin(p.theta) * np.cos(p.phi)
        y = p.r * np.sin(p.theta) * np.sin(p.phi)
        z = p.r * np.cos(p.theta)
        self.point = np.array([x, y, z])

    def __copy__(self):
        return Cartesian(self.point)

    @dispatch
    def __add__(self, other: "Cartesian") -> "Cartesian":
        return Cartesian(self.point + other.point)

    @dispatch
    def __add__(self, other: "Spherical") -> "Cartesian":
        return self + Cartesian(other)

    @dispatch
    def __sub__(self, other: "Spherical") -> "Cartesian":
        return self - Cartesian(other)

    @dispatch
    def __eq__(self, other: "Cartesian"):
        return np.allclose(self.point, other.point)

    @dispatch
    def __eq__(self, other: "Spherical"):
        return self == Cartesian(other)

    @dispatch
    def __sub__(self, other: "Cartesian"):
        return Cartesian(self.point - other.point)

    @dispatch
    def __mul__(self, other: Number):
        return Cartesian(self.point * other)

    @dispatch
    def __getitem__(self, key: int):
        return self.point[key]

    @dispatch
    def __getitem__(self, key: str):
        if key == "x":
            return self.x
        elif key == "y":
            return self.y
        elif key == "z":
            return self.z
        else:
            raise KeyError("Cartesians have keys x, y and z.")

    @dispatch
    def __setitem__(self, key: int, value: Number):
        self.point[key] = value

    @dispatch
    def __setitem__(self, key: str, value: Number):
        if key == "x":
            self.point[0] = value
        elif key == "y":
            self.point[1] = value
        elif key == "z":
            self.point[2] = value
        else:
            raise KeyError("Cartesians have keys x, y and z.")

    def __str__(self):
        return f"Cartesian({', '.join(map(str, self.point))})"

    def __repr__(self):
        return f"Cartesian([{', '.join(map(str, self.point))}])"

    def __bool__(self):
        return bool(np.any(self.point))

    def __abs__(self):
        return np.linalg.norm(self.point)

    @property
    def x(self):
        return self.point[0]

    @property
    def y(self):
        return self.point[1]

    @property
    def z(self):
        return self.point[2]

    @x.setter
    def x(self, new: float):
        self.point[0] = new

    @y.setter
    def y(self, new: float):
        self.point[1] = new

    @z.setter
    def z(self, new: float):
        self.point[2] = new


class Spherical(Coordinate):
    _r: float
    _theta: float
    _phi: float
    unique: bool = False

    @dispatch
    def __init__(self, point: Union[list, np.ndarray], unique=False):
        self._r = point[0]
        self._theta = point[1]
        self._phi = point[2]
        self.unique = unique
        if self.unique:
            self.simplify()

    @dispatch
    def __init__(self, point: Cartesian, unique=False):
        self._r = np.linalg.norm([point.x, point.y, point.z])
        self._theta = np.arccos(point.z / self.r)
        self._phi = np.arctan2(point.y, point.x)
        self.unique = unique

    @dispatch
    def __init__(self, point: "Spherical", unique: Optional[bool] = None):
        self._r = point.r
        self._theta = point.theta
        self._phi = point.phi
        self.unique = point.unique if unique is None else unique
        if self.unique:
            self.simplify()

    @property
    def r(self):
        return self._r

    @property
    def theta(self):
        return self._theta

    @property
    def phi(self):
        return self._phi

    @r.setter
    def r(self, new):
        self._r = new
        if new < 0 and self.unique:
            self.simplify()

    @theta.setter
    def theta(self, new):
        self._theta = new
        if not 0 <= new <= np.pi and self.unique:
            self.simplify()

    @phi.setter
    def phi(self, new):
        self._phi = new % (2 * np.pi) if self.unique else new

    def __copy__(self):
        return Spherical([self.r, self.theta, self.phi])

    @dispatch
    def __add__(self, other: "Spherical") -> "Spherical":
        return Spherical(Cartesian(self) + Cartesian(other))

    @dispatch
    def __add__(self, other: Cartesian) -> Cartesian:
        return Cartesian(self) + other

    @dispatch
    def __sub__(self, other: "Spherical") -> "Spherical":
        return Spherical(Cartesian(self) - Cartesian(other))

    @dispatch
    def __sub__(self, other: Cartesian) -> "Spherical":
        return Spherical(Cartesian(self) - other)

    @dispatch
    def __mul__(self, other: Number) -> "Spherical":
        return Spherical([self.r * other, self.theta, self.phi])

    @dispatch
    def __eq__(self, other: Cartesian):
        return Cartesian(self) == other

    @dispatch
    def __eq__(self, other: "Spherical"):
        # TODO: write a decent implementation. there's no need to convert them.
        if not other.unique:
            other = Spherical(other, unique=True)

        if self.unique:
            return np.allclose(
                [self.r, self.theta, self.phi], [other.r, other.theta, other.phi]
            )
        else:
            s = Spherical(self, unique=True)
            return np.allclose([s.r, s.theta, s.phi], [other.r, other.theta, other.phi])

    def __abs__(self):
        return abs(self.r)

    def __str__(self):
        return f"Spherical({self.r}, {self.theta}, {self.phi})"

    def __repr__(self):
        return f"Spherical([{self.r}, {self.theta}, {self.phi}])"

    def __bool__(self):
        return np.isclose(self.r, 0)

    def simplify(self):
        """Simplifies the Spherical Coordinate ensuring r ∈ [0, ∞), θ ∈ [0, π] and φ ∈ [0, 2π)."""
        r, theta, phi = self._r, self._theta, self._phi
        # Constraint 1: r ≥ 0
        if r < 0:
            r *= -1
            theta = np.pi - theta
            phi += np.pi

        # Constraint 2: 0 ≤ θ ≤ π
        theta = theta % (2 * np.pi)  # take off full revolutions
        if theta > np.pi:
            theta = 2 * np.pi - theta
            phi += np.pi  # θ → θ - π ⇒ r → -r, so we correct this.

        # Constraint 3: 0 ≤ φ < 2π
        phi = phi % (2 * np.pi)
        self._r, self._theta, self._phi = r, theta, phi
        return self
