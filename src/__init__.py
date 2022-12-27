from abc import ABC
from numbers import Number
from typing import Union

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
    def __init__(self, point: 'Cartesian'):
        self = point

    @dispatch
    def __init__(self, p: 'Spherical'):
        x = p.r * np.sin(p.theta) * np.cos(p.phi)
        y = p.r * np.sin(p.theta) * np.sin(p.phi)
        z = p.r * np.cos(p.theta)
        self.point = np.array([x, y, z])

    @dispatch
    def __add__(self, other: 'Cartesian') -> 'Cartesian':
        return Cartesian(self.point + other.point)

    @dispatch
    def __add__(self, other: 'Spherical') -> 'Cartesian':
        return self + Cartesian(other)

    @dispatch
    def __sub__(self, other: 'Spherical') -> 'Cartesian':
        return self - Cartesian(other)

    @dispatch
    def __eq__(self, other: 'Cartesian'):
        return np.allclose(self.point, other.point)

    @dispatch
    def __eq__(self, other: 'Spherical'):
        return self == Cartesian(other)

    @dispatch
    def __sub__(self, other: 'Cartesian'):
        return Cartesian(self.point - other.point)

    @dispatch
    def __mul__(self, other: Number):
        return Cartesian(self.point * other)

    @dispatch
    def __getitem__(self, key: int):
        return self.point[key]

    @dispatch
    def __getitem__(self, key: str):
        if key == 'x':
            return self.x
        elif key == 'y':
            return self.y
        elif key == 'z':
            return self.z
        else:
            raise KeyError("Cartesians have keys x, y and z.")

    @dispatch
    def __setitem__(self, key: int, value: Number):
        self.point[key] = value

    @dispatch
    def __setitem__(self, key: str, value: Number):
        if key == 'x':
            self.point[0] = value
        elif key == 'y':
            self.point[1] = value
        elif key == 'z':
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
    r: Number
    theta: Number
    phi: Number

    @dispatch
    def __init__(self, point: Union[list, np.ndarray]):
        self.r = point[0]
        self.theta = point[1]
        self.phi = point[2]

    @dispatch
    def __init__(self, point: Cartesian):
        self.r = np.linalg.norm([point.x, point.y, point.z])
        self.theta = np.arccos(point.z / self.r)
        self.phi = np.arctan2(point.y, point.x)

    @dispatch
    def __init__(self, point: 'Spherical'):
        self = point

    @dispatch
    def __add__(self, other: 'Spherical') -> 'Spherical':
        return Spherical(Cartesian(self) + Cartesian(other))

    @dispatch
    def __add__(self, other: Cartesian) -> Cartesian:
        return Cartesian(self) + other

    @dispatch
    def __sub__(self, other: 'Spherical') -> 'Spherical':
        return Spherical(Cartesian(self) - Cartesian(other))

    @dispatch
    def __sub__(self, other: Cartesian) -> 'Spherical':
        return Spherical(Cartesian(self) - other)

    @dispatch
    def __mul__(self, other: Number) -> 'Spherical':
        return Spherical([self.r * other, self.theta, self.phi])

    @dispatch
    def __eq__(self, other: Cartesian):
        return Cartesian(self) == other

    @dispatch
    def __eq__(self, other: 'Spherical'):
        # TODO: write a decent implementation. there's no need to convert them.
        return Cartesian(self) == Cartesian(other)

    def __abs__(self):
        return abs(self.r)

    def __str__(self):
        return f"Spherical({self.r}, {self.theta}, {self.phi})"

    def __repr__(self):
        return f"Spherical([{self.r}, {self.theta}, {self.phi}])"

    def __bool__(self):
        return np.isclose(self.r, 0)
