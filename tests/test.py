import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

import unittest

from src import *

class TestBasics(unittest.TestCase):
    def test_basics(self):
        c = Cartesian([1, 2, 3])
        s = Spherical([2, np.pi/2, np.pi])
        self.assertEqual(c, c)
        self.assertEqual(s, s)
        self.assertEqual(Cartesian([0,0,1]), Spherical([1,0,0]))
        self.assertEqual(Cartesian([-2.4492935982947064e-16,5.99903913064743e-32,1.0]), Spherical([1,0,0]))


class TestCartesianArithmetic(unittest.TestCase):

    def test_sum(self):
        c = Cartesian([1, 2, 3])
        c2 = Cartesian([4, 2, 3])
        self.assertEqual(c+c2, Cartesian([5, 4, 6]))
    def test_sub(self):
        c = Cartesian([1, 2, 3])
        c2 = Cartesian([4, 2, 3])
        self.assertEqual(c2-c, Cartesian([3, 0, 0]))
    def test_scalar_mul(self):
        c = Cartesian([1, 2, 3])
        self.assertEqual(c * 2, Cartesian([2, 4, 6]))

class TestSphericalArithmetic(unittest.TestCase):
    def test_sum(self):
        c = Spherical([1, 2, 3])
        c2 = Spherical([4, 2, 3])
        self.assertAlmostEqual(c+c2, Spherical([5, 2, 3]))

class TestConversions(unittest.TestCase):
    def test_sum(self):
        c = Cartesian([1, 2, 3])
        s = Spherical([2, np.pi/2, np.pi])
        self.assertAlmostEqual(c+s, Cartesian([-1.0, 2.0, 3.0]))
        self.assertAlmostEqual(c+s, s+c)




if __name__ == '__main__':
    unittest.main()