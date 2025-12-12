import re
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO

from fraocme.common import parser
from fraocme.common.printer import (
    print_dict_head,
    print_dict_row,
    print_max_in_rows,
    print_ranges,
    print_row_stats,
)
from fraocme.common.range_utils import (
    merge_ranges,
    range_coverage,
    range_intersection,
    ranges_overlap,
    within_range,
)
from fraocme.common.sequence_utils import (
    all_equal,
    chunks,
    flatten,
    frequencies,
    pairwise,
    rotate,
    unique,
    windows,
)
from fraocme.common.utils import (
    digits,
    divisors,
    euclidean_distance,
    from_digits,
    gcd,
    lcm,
    sign,
    squared_euclidean_distance,
    wrap,
)

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


class TestCommonPrinter(unittest.TestCase):
    """Test common printer functions."""

    def test_print_max_in_rows_basic(self):
        """Test print_max_in_rows prints max of each row."""
        grid = [[1, 5, 3], [2, 4, 6], [7, 2, 1]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["5", "6", "7"])

    def test_print_max_in_rows_single_row(self):
        """Test print_max_in_rows with single row."""
        grid = [[1, 5, 3]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertEqual(output, "5")

    def test_print_max_in_rows_single_element(self):
        """Test print_max_in_rows with single element per row."""
        grid = [[1], [5], [3]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["1", "5", "3"])

    def test_print_max_in_rows_empty_row(self):
        """Test print_max_in_rows handles empty row."""
        grid = [[1, 2], [], [3, 4]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output[0], "2")
        self.assertEqual(output[1], "Empty row")
        self.assertEqual(output[2], "4")

    def test_print_max_in_rows_negative_numbers(self):
        """Test print_max_in_rows with negative numbers."""
        grid = [[-1, -5, -3], [-2, -4, -6]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["-1", "-2"])

    def test_print_max_in_rows_mixed_numbers(self):
        """Test print_max_in_rows with mixed positive/negative numbers."""
        grid = [[1, -5, 3], [-2, 4, -6]]

        captured_output = StringIO()
        sys.stdout = captured_output
        print_max_in_rows(grid)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip().split("\n")
        self.assertEqual(output, ["3", "4"])


class TestCommonParser(unittest.TestCase):
    def test_sections(self):
        raw = "a\nb\n\nc\n"
        self.assertEqual(parser.sections(raw), ["a\nb", "c"])

    def test_lines_and_ints(self):
        raw = "1\n2\n-3"
        self.assertEqual(parser.lines(raw), ["1", "2", "-3"])
        self.assertEqual(parser.ints(raw), [1, 2, -3])

    def test_key_ints(self):
        raw = "190: 10 19\n83: 17 5"
        self.assertEqual(parser.key_ints(raw), {190: [10, 19], 83: [17, 5]})

    def test_ranges(self):
        raw = "1-5,10-12,20-20"
        self.assertEqual(parser.ranges(raw), [(1, 5), (10, 12), (20, 20)])

    def test_mapped(self):
        raw = "1,2\n3,4"
        result = parser.mapped(raw, lambda line: tuple(map(int, line.split(","))))
        self.assertEqual(result, [(1, 2), (3, 4)])

    def test_coordinates(self):
        raw = "10,20\n30,40\n50,60"
        self.assertEqual(parser.coordinates(raw), [(10, 20), (30, 40), (50, 60)])

    def test_coordinates_3d(self):
        raw = "1,2,3\n4,5,6\n7,8,9"
        self.assertEqual(parser.coordinates(raw), [(1, 2, 3), (4, 5, 6), (7, 8, 9)])

    def test_coordinates_with_delimiter(self):
        raw = "10 20\n30 40"
        self.assertEqual(parser.coordinates(raw, delimiter=" "), [(10, 20), (30, 40)])

    def test_coordinates_with_float(self):
        raw = "1.5,2.5\n3.5,4.5"
        self.assertEqual(
            parser.coordinates(raw, value_type=float), [(1.5, 2.5), (3.5, 4.5)]
        )

    def test_coordinates_inline_space_separated(self):
        """Test inline coordinates separated by spaces: '1,2 3,4 5,6'"""
        raw = "1,2 3,4 5,6"
        self.assertEqual(
            parser.coordinates(raw, coord_delimiter=" "), [(1, 2), (3, 4), (5, 6)]
        )

    def test_coordinates_inline_dash_notation(self):
        """Test inline coordinates with dash notation: '1-2 3-4 5-6'"""
        raw = "1-2 3-4 5-6"
        self.assertEqual(
            parser.coordinates(raw, delimiter="-", coord_delimiter=" "),
            [(1, 2), (3, 4), (5, 6)],
        )

    def test_coordinates_inline_comma_separated(self):
        """Test inline coordinates separated by commas: '1-2,3-4,5-6'"""
        raw = "1-2,3-4,5-6"
        self.assertEqual(
            parser.coordinates(raw, delimiter="-", coord_delimiter=","),
            [(1, 2), (3, 4), (5, 6)],
        )

    def test_coordinates_named_with_mapped(self):
        """Test parsing named coordinates like 'x=1, y=2, z=3' using mapped."""
        import re

        raw = "x=10, y=20, z=30\nx=40, y=50, z=60"
        result = parser.mapped(
            raw,
            lambda line: tuple(int(x) for x in re.findall(r"-?\d+", line)),
        )
        self.assertEqual(result, [(10, 20, 30), (40, 50, 60)])


class TestCommonUtils(unittest.TestCase):
    def test_frequencies_and_all_equal(self):
        data = ["a", "b", "a", "c", "a", "b"]
        self.assertEqual(frequencies(data), {"a": 3, "b": 2, "c": 1})
        self.assertTrue(all_equal([7, 7, 7]))
        self.assertFalse(all_equal([1, 2, 1]))
        self.assertTrue(all_equal([]))

    def test_chunks_windows_pairwise(self):
        data = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(chunks(data, 3), [[1, 2, 3], [4, 5, 6], [7]])
        self.assertEqual(windows([1, 2, 3, 4], 2), [[1, 2], [2, 3], [3, 4]])
        self.assertEqual(pairwise([1, 2, 3, 4]), [(1, 2), (2, 3), (3, 4)])

    def test_rotate_unique_flatten(self):
        self.assertEqual(rotate([1, 2, 3, 4, 5], -2), [3, 4, 5, 1, 2])
        self.assertEqual(rotate([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3])
        self.assertEqual(rotate([], 3), [])
        self.assertEqual(unique([1, 2, 2, 3, 1, 4, 2]), [1, 2, 3, 4])
        self.assertEqual(flatten([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])

    def test_sign_digits_wrap(self):
        self.assertEqual(sign(5), 1)
        self.assertEqual(sign(-3), -1)
        self.assertEqual(sign(0), 0)
        self.assertEqual(digits(-987), [9, 8, 7])
        self.assertEqual(wrap(105, 100), 5)
        self.assertEqual(wrap(-10, 100), 90)

    def test_number_theory_helpers(self):
        self.assertEqual(divisors(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(gcd(24, 36, 18), 6)
        self.assertEqual(lcm(3, 4, 5), 60)
        self.assertEqual(from_digits([9, 8, 7]), 987)

    def test_euclidean_distance_2d(self):
        """Test 2D Euclidean distance."""
        # Basic 3-4-5 triangle
        self.assertEqual(euclidean_distance((0, 0), (3, 4)), 5.0)
        # Same point
        self.assertEqual(euclidean_distance((5, 5), (5, 5)), 0.0)
        # With floats
        self.assertEqual(euclidean_distance((1.5, 2.5), (4.5, 6.5)), 5.0)

    def test_euclidean_distance_3d(self):
        """Test 3D Euclidean distance (junction boxes)."""
        dist = euclidean_distance((162, 817, 812), (57, 618, 57))
        self.assertAlmostEqual(dist, 787.814064, places=5)

        dist2 = euclidean_distance((162, 817, 812), (906, 360, 560))
        self.assertAlmostEqual(dist2, 908.784353, places=5)

    def test_euclidean_distance_different_dimensions(self):
        """Test that different dimensions raise ValueError."""
        with self.assertRaises(ValueError) as context:
            euclidean_distance((1, 2), (1, 2, 3))
        self.assertIn("same dimensions", str(context.exception))

    def test_squared_euclidean_distance_2d(self):
        """Test 2D squared Euclidean distance."""
        self.assertEqual(squared_euclidean_distance((0, 0), (3, 4)), 25.0)
        self.assertEqual(squared_euclidean_distance((5, 5), (5, 5)), 0.0)

    def test_squared_euclidean_distance_3d(self):
        """Test 3D squared Euclidean distance."""
        sq_dist = squared_euclidean_distance((162, 817, 812), (57, 618, 57))
        self.assertEqual(sq_dist, 620651.0)

    def test_squared_euclidean_distance_comparison(self):
        """Test using squared distance for comparison (optimization)."""
        box1 = (162, 817, 812)
        box2 = (57, 618, 57)
        box3 = (906, 360, 560)

        dist_to_box2 = squared_euclidean_distance(box1, box2)
        dist_to_box3 = squared_euclidean_distance(box1, box3)

        self.assertLess(dist_to_box2, dist_to_box3)

    def test_squared_euclidean_distance_different_dimensions(self):
        """Test that different dimensions raise ValueError for squared distance."""
        with self.assertRaises(ValueError) as context:
            squared_euclidean_distance((1, 2), (1, 2, 3))
        self.assertIn("same dimensions", str(context.exception))

    def test_range_helpers(self):
        self.assertTrue(ranges_overlap((1, 5), (5, 10)))
        self.assertFalse(ranges_overlap((1, 3), (4, 6)))

        self.assertEqual(range_intersection((1, 10), (5, 15)), (5, 10))
        self.assertIsNone(range_intersection((1, 5), (7, 10)))

        merged = merge_ranges([(10, 15), (1, 5), (3, 8), (16, 18)], inclusive=False)

        self.assertEqual(merged, [(1, 8), (10, 15), (16, 18)])

        self.assertTrue(within_range(5, [(1, 5), (10, 15)], inclusive=True))
        self.assertFalse(within_range(5, [(1, 5), (10, 15)], inclusive=False))

        from fraocme.common import RangeMode

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


class TestCommonPrinterExtras(unittest.TestCase):
    def test_print_row_stats_empty_and_basic(self):
        buf = StringIO()
        with redirect_stdout(buf):
            print_row_stats([])
        self.assertIn("Empty row", buf.getvalue())

        buf = StringIO()
        with redirect_stdout(buf):
            print_row_stats([1, 2, 4, 4])
        output = strip_ansi(buf.getvalue())
        self.assertIn("Min", output)
        self.assertIn("Max", output)
        self.assertIn("Med", output)
        self.assertIn("Avg", output)
        self.assertIn("[", output)

    def test_print_ranges_empty_and_basic(self):
        buf = StringIO()
        with redirect_stdout(buf):
            print_ranges([])
        self.assertIn("No ranges", buf.getvalue())

        buf = StringIO()
        with redirect_stdout(buf):
            print_ranges([(1, 3), (5, 6)], width=10, head=None)
        output = strip_ansi(buf.getvalue())
        self.assertIn("Ranges", output)
        self.assertIn("1-3", output)
        self.assertIn("5-6", output)

    def test_print_dict_row(self):
        data = {190: [10, 19], 83: [17, 5]}

        buf = StringIO()
        with redirect_stdout(buf):
            print_dict_row(data, 999)
        self.assertIn("Key not found", buf.getvalue())

        buf = StringIO()
        with redirect_stdout(buf):
            print_dict_row(data, 190)
        output = strip_ansi(buf.getvalue())
        self.assertIn("190", output)
        self.assertIn("10", output)
        self.assertIn("19", output)

    def test_print_dict_head(self):
        empty_buf = StringIO()
        with redirect_stdout(empty_buf):
            print_dict_head({})
        self.assertIn("Empty dict", empty_buf.getvalue())

        data = {190: [10, 19], 83: [17, 5], 3267: [81, 40, 27]}
        buf = StringIO()
        with redirect_stdout(buf):
            print_dict_head(data, n=2)
        output = strip_ansi(buf.getvalue())
        self.assertIn("Keys", output)
        self.assertIn("Values", output)
        self.assertIn("... and 1 more", output)


if __name__ == "__main__":
    unittest.main()
