import unittest

from fraocme.common import RangeMode
from fraocme.common.range_utils import (
    merge_ranges,
    range_coverage,
    range_intersection,
    ranges_overlap,
    subtract_interval,
    within_range,
)


class TestRangeUtils(unittest.TestCase):
    def test_ranges_overlap_and_intersection(self):
        self.assertTrue(ranges_overlap((1, 5), (5, 10)))
        self.assertFalse(ranges_overlap((1, 3), (4, 6)))

        self.assertEqual(range_intersection((1, 10), (5, 15)), (5, 10))
        self.assertIsNone(range_intersection((1, 5), (7, 10)))

    def test_merge_and_within(self):
        merged = merge_ranges([(10, 15), (1, 5), (3, 8), (16, 18)], inclusive=False)

        self.assertEqual(merged, [(1, 8), (10, 15), (16, 18)])

        self.assertTrue(within_range(5, [(1, 5), (10, 15)], inclusive=True))
        self.assertFalse(within_range(5, [(1, 5), (10, 15)], inclusive=False))

    def test_range_coverage_modes(self):
        self.assertEqual(
            range_coverage([(1, 3), (5, 7), (2, 6)], mode=RangeMode.INCLUSIVE), 7
        )
        self.assertEqual(
            range_coverage([(1, 3), (5, 7), (2, 6)], mode=RangeMode.HALF_OPEN), 6
        )
        self.assertEqual(
            range_coverage([(1, 3), (5, 7), (2, 6)], mode=RangeMode.EXCLUSIVE), 5
        )

    def test_merge_ranges_empty(self):
        self.assertEqual(merge_ranges([], inclusive=True), [])

    def test_within_range_exclusive_hit(self):
        self.assertTrue(within_range(5, [(4, 6)], inclusive=False))

    def test_subtract_interval_internal(self):
        # remove inside base -> two pieces
        self.assertEqual(subtract_interval((1, 10), (3, 5)), [(1, 2), (6, 10)])

    def test_subtract_interval_touching(self):
        # remove touches endpoint -> remaining adjusts accordingly
        self.assertEqual(subtract_interval((1, 5), (5, 10)), [(1, 4)])


if __name__ == "__main__":
    unittest.main()
