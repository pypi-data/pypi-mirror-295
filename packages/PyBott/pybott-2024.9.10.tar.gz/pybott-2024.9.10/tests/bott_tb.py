"""
Unit tests for the Bott index calculation on the Haldane model.

These tests ensure that the Bott index is correctly calculated for different values of t2 and delta,
accounting for floating-point precision issues by using a tolerance.

Test Cases:
-----------
1. test_bott_index_t2_less_than_delta:
    Verifies that the Bott index is approximately zero when 3*sqrt(3)*t2 < delta.
    Uses a tolerance to account for small deviations due to floating-point calculations.

2. test_bott_index_t2_greater_than_delta:
    Ensures that the Bott index is approximately 1 or -1 when 3*sqrt(3)*t2 > delta.
    The test checks if the result is close enough to these values, again using a small tolerance.

Tolerance:
----------
A small tolerance (epsilon = 1e-6) is applied in these tests to handle the floating-point precision 
issues that may arise during the calculation of the Bott index.
"""

import unittest

import haldane
import bott


class TestBottIndex(unittest.TestCase):
    """
    TestBottIndex: Unit tests for the Bott index calculation in the Haldane model.
    
    This class contains unit tests to verify that the Bott index is correctly calculated 
    for various parameter values of t2 and delta, considering floating-point precision 
    through a tolerance.

    Attributes:
    -----------
    n_side : int
    The size of the grid used in the Haldane model.
    t1 : float
    The first parameter of the Haldane model.
    energy_in_gap : float
    The energy level in the gap used during the Bott index calculation.
    epsilon : float
    The tolerance used for comparing floating-point results to account for precision errors.
    """
    def setUp(self):
        """
        This method runs before each test to initialize common parameters.
        """
        self.n_side = 10  # Grid size
        self.t1 = 1  # First parameter of the Haldane model
        self.energy_in_gap = 0  # Energy level in the gap
        self.epsilon = 1e-6  # Tolerance for floating-point comparison

    def test_bott_index_t2_less_than_delta(self):
        """
        Test that the Bott index is zero when 3*sqrt(3)*t2 < delta
        """
        t2 = 0.1j
        delta = 1

        grid, eigenvalues, eigenvectors = haldane.haldane_model(
            n_side=self.n_side, t1=self.t1, t2=t2, delta=delta, pbc=False
        )

        b = bott.bott(grid, eigenvectors, eigenvalues, self.energy_in_gap)
        self.assertAlmostEqual(
            b,
            0,
            delta=self.epsilon,
            msg="The Bott index should be 0 for 3*sqrt(3)t2 < delta.",
        )

    def test_bott_index_t2_greater_than_delta(self):
        """
        Test that the Bott index is 1 or -1 when 3*sqrt(3)*t2 > delta
        """
        t2 = 0.5j
        delta = 0

        grid, eigenvalues, eigenvectors = haldane.haldane_model(
            n_side=self.n_side, t1=self.t1, t2=t2, delta=delta, pbc=False
        )

        b = bott.bott(grid, eigenvectors, eigenvalues, self.energy_in_gap)
        self.assertTrue(
            abs(b - 1) < self.epsilon or abs(b + 1) < self.epsilon,
            "The Bott index should be 0 for 3*sqrt(3)t2 < delta.",
        )


if __name__ == "__main__":
    unittest.main()
