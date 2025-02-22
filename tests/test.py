import os
import sys

import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "coordsystems")
)

π = np.pi

import unittest

from coordsystems import Cartesian, Spherical


class TestBasics(unittest.TestCase):
    def test_basics(self):
        c = Cartesian([1, 2, 3])
        s = Spherical([2, np.pi / 2, np.pi])
        self.assertEqual(c, c)
        self.assertEqual(s, s)
        self.assertEqual(Cartesian([0, 0, 1]), Spherical([1, 0, 0]))
        self.assertEqual(
            Cartesian([-2.4492935982947064e-16, 5.99903913064743e-32, 1.0]),
            Spherical([1, 0, 0]),
        )


class TestCartesianArithmetic(unittest.TestCase):
    def test_sum(self):
        c = Cartesian([1, 2, 3])
        c2 = Cartesian([4, 2, 3])
        self.assertEqual(c + c2, Cartesian([5, 4, 6]))

    def test_sub(self):
        c = Cartesian([1, 2, 3])
        c2 = Cartesian([4, 2, 3])
        self.assertEqual(c2 - c, Cartesian([3, 0, 0]))

    def test_scalar_mul(self):
        c = Cartesian([1, 2, 3])
        self.assertEqual(c * 2, Cartesian([2, 4, 6]))


class TestSphericalArithmetic(unittest.TestCase):
    def test_sum(self):
        c = Spherical([1, 2, 3])
        c2 = Spherical([4, 2, 3])
        self.assertAlmostEqual(c + c2, Spherical([5, 2, 3]))


class TestConversions(unittest.TestCase):
    def test_sum(self):
        c = Cartesian([1, 2, 3])
        s = Spherical([2, np.pi / 2, np.pi])
        self.assertAlmostEqual(c + s, Cartesian([-1.0, 2.0, 3.0]))
        self.assertAlmostEqual(c + s, s + c)


class TestSphericalSimplify(unittest.TestCase):
    def isUniqueSpheric(self, s: Spherical) -> bool:
        if s.r < 0:
            return False
        if not 0 <= s.theta <= π:
            return False
        if not 0 <= s.phi < 2 * π:
            return False
        return True

    def assertUniqueSpheric(self, s: Spherical):
        self.assertGreaterEqual(s.r, 0)
        self.assertGreaterEqual(s.theta, 0)
        self.assertLessEqual(s.theta, π)
        self.assertGreaterEqual(s.phi, 0)
        self.assertLess(s.phi, 2 * π)

    def test_theta(self):
        s1 = Spherical([2, 3 * π, π], unique=False)
        s2 = Spherical([2, 3 * π, π], unique=True)
        self.assertEqual(s1, s2)
        self.assertEqual(Cartesian(s1), Cartesian(s2))
        self.assertFalse(self.isUniqueSpheric(s1))
        self.assertUniqueSpheric(s2)

    def test_phi(self):
        s1 = Spherical([2, π, 7 * π / 2], unique=False)
        s2 = Spherical([2, π, 7 * π / 2], unique=True)
        self.assertEqual(s1, s2)
        self.assertEqual(Cartesian(s1), Cartesian(s2))
        self.assertFalse(self.isUniqueSpheric(s1))
        self.assertUniqueSpheric(s2)

    def test_radius(self):
        s1 = Spherical([-2, π, π / 2], unique=False)
        s2 = Spherical([-2, π, π / 2], unique=True)
        self.assertEqual(s1, s2)
        self.assertEqual(Cartesian(s1), Cartesian(s2))
        self.assertFalse(self.isUniqueSpheric(s1))
        self.assertUniqueSpheric(s2)


if __name__ == "__main__":
    unittest.main()
