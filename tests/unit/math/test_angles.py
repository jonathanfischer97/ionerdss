import unittest
import numpy as np
from ionerdss.math.angles import absolute_error_to_angle, angles_between_vector_and_vectors

class TestAngles(unittest.TestCase):

    def test_absolute_error_to_angle_basic(self):
        points = np.array([[1, 0, 0], [0, 2, 0], [0, 0, 4]])
        error = 0.1
        expected = np.array([0.1 / 1, 0.1 / 2, 0.1 / 4])
        result = absolute_error_to_angle(error, points)
        np.testing.assert_allclose(result, expected, rtol=1e-6)

    def test_absolute_error_to_angle_with_small_radius(self):
        points = np.array([[0, 0, 0], [1e-12, 0, 0]])
        error = 0.1
        result = absolute_error_to_angle(error, points, tol=1e-8)
        self.assertTrue(np.all(result >= 0))
        self.assertAlmostEqual(result[0], 0.1 / 1e-8)
        self.assertAlmostEqual(result[1], 0.1 / 1e-8)

    def test_angles_between_vector_and_vectors_basic(self):
        ref = np.array([1, 0, 0])
        angle_deg = 47.3
        angle_rad = np.deg2rad(angle_deg)
        target_47_3 = np.array([np.cos(angle_rad), np.sin(angle_rad), 0])

        targets = np.array([
            [1, 0, 0],       # 0 degrees
            [0, 1, 0],       # 90 degrees
            [-1, 0, 0],      # 180 degrees
            [1, 1, 0],       # ~45 degrees
            target_47_3,     # 47.3 degrees
        ])

        result = angles_between_vector_and_vectors(ref, targets)
        expected = np.array([
            0.0,
            np.pi / 2,
            np.pi,
            np.pi / 4,
            angle_rad,
        ])
        np.testing.assert_allclose(result, expected, rtol=1e-6)

    def test_angles_between_vector_and_zero_vector(self):
        ref = np.array([1, 0, 0])
        targets = np.array([
            [0, 0, 0],  # zero norm
            [0, 0, 0],  # zero norm
        ])
        result = angles_between_vector_and_vectors(ref, targets)
        expected = np.array([0.0, 0.0])
        np.testing.assert_array_equal(result, expected)

    def test_angles_between_vector_and_vectors_with_tolerance(self):
        ref = np.array([1e-12, 0, 0])
        targets = np.array([[1, 0, 0]])
        result = angles_between_vector_and_vectors(ref, targets, tol=1e-8)
        expected = np.array([0.0])  # Denominator too small, treated as 0
        np.testing.assert_array_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
