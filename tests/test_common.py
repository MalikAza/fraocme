import re
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO

from fraocme.common import parser
from fraocme.common import utils as common_utils
from fraocme.common.printer import (
    print_dict_head,
    print_dict_row,
    print_max_in_rows,
    print_ranges,
    print_row_stats,
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


class TestCommonUtils(unittest.TestCase):
    def test_frequencies_and_all_equal(self):
        data = ["a", "b", "a", "c", "a", "b"]
        self.assertEqual(common_utils.frequencies(data), {"a": 3, "b": 2, "c": 1})
        self.assertTrue(common_utils.all_equal([7, 7, 7]))
        self.assertFalse(common_utils.all_equal([1, 2, 1]))
        self.assertTrue(common_utils.all_equal([]))

    def test_chunks_windows_pairwise(self):
        data = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual(common_utils.chunks(data, 3), [[1, 2, 3], [4, 5, 6], [7]])
        self.assertEqual(
            common_utils.windows([1, 2, 3, 4], 2), [[1, 2], [2, 3], [3, 4]]
        )
        self.assertEqual(common_utils.pairwise([1, 2, 3, 4]), [(1, 2), (2, 3), (3, 4)])

    def test_rotate_unique_flatten(self):
        self.assertEqual(common_utils.rotate([1, 2, 3, 4, 5], -2), [3, 4, 5, 1, 2])
        self.assertEqual(common_utils.rotate([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3])
        self.assertEqual(common_utils.rotate([], 3), [])
        self.assertEqual(common_utils.unique([1, 2, 2, 3, 1, 4, 2]), [1, 2, 3, 4])
        self.assertEqual(common_utils.flatten([[1, 2], [3, 4], [5]]), [1, 2, 3, 4, 5])

    def test_sign_digits_wrap(self):
        self.assertEqual(common_utils.sign(5), 1)
        self.assertEqual(common_utils.sign(-3), -1)
        self.assertEqual(common_utils.sign(0), 0)
        self.assertEqual(common_utils.digits(-987), [9, 8, 7])
        self.assertEqual(common_utils.wrap(105, 100), 5)
        self.assertEqual(common_utils.wrap(-10, 100), 90)

    def test_number_theory_helpers(self):
        self.assertEqual(common_utils.divisors(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(common_utils.gcd(24, 36, 18), 6)
        self.assertEqual(common_utils.lcm(3, 4, 5), 60)
        self.assertEqual(common_utils.from_digits([9, 8, 7]), 987)

    def test_range_helpers(self):
        self.assertTrue(common_utils.ranges_overlap((1, 5), (5, 10)))
        self.assertFalse(common_utils.ranges_overlap((1, 3), (4, 6)))

        self.assertEqual(common_utils.range_intersection((1, 10), (5, 15)), (5, 10))
        self.assertIsNone(common_utils.range_intersection((1, 5), (7, 10)))

        merged = common_utils.merge_ranges(
            [(10, 15), (1, 5), (3, 8), (16, 18)], inclusive=False
        )

        self.assertEqual(merged, [(1, 8), (10, 15), (16, 18)])

        self.assertTrue(
            common_utils.within_range(5, [(1, 5), (10, 15)], inclusive=True)
        )
        self.assertFalse(
            common_utils.within_range(5, [(1, 5), (10, 15)], inclusive=False)
        )

        # Test with new RangeMode API
        from fraocme.common import RangeMode

        self.assertEqual(
            common_utils.range_coverage(
                [(1, 3), (5, 7), (2, 6)], mode=RangeMode.INCLUSIVE
            ),
            7,
        )
        self.assertEqual(
            common_utils.range_coverage(
                [(1, 3), (5, 7), (2, 6)], mode=RangeMode.HALF_OPEN
            ),
            6,
        )
        self.assertEqual(
            common_utils.range_coverage(
                [(1, 3), (5, 7), (2, 6)], mode=RangeMode.EXCLUSIVE
            ),
            5,
        )

    def test_merge_ranges_empty(self):
        self.assertEqual(common_utils.merge_ranges([], inclusive=True), [])

    def test_within_range_exclusive_hit(self):
        self.assertTrue(common_utils.within_range(5, [(4, 6)], inclusive=False))


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
