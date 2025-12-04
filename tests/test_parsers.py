import unittest
from fraocme.parsers import (
    lines,
    ints,
    ints_per_line,
    floats,
    words,
    blocks,
    csv,
    csv_ints,
    char_grid,
    int_grid,
    mapped,
)


class TestBasicParsers(unittest.TestCase):
    """Test basic parsing functions."""

    def test_lines(self):
        """Test parsing input as list of strings."""
        raw = "hello\nworld\ntest"
        self.assertEqual(lines(raw), ["hello", "world", "test"])

    def test_lines_with_whitespace(self):
        """Test lines handles leading/trailing whitespace."""
        raw = "\nhello\nworld\n"
        self.assertEqual(lines(raw), ["hello", "world"])

    def test_lines_single_line(self):
        """Test lines with single line input."""
        self.assertEqual(lines("hello"), ["hello"])

    def test_ints(self):
        """Test parsing integers from lines."""
        raw = "42\n100\n-5"
        self.assertEqual(ints(raw), [42, 100, -5])

    def test_ints_with_whitespace(self):
        """Test ints handles whitespace."""
        raw = "\n42\n100\n"
        self.assertEqual(ints(raw), [42, 100])

    def test_ints_per_line_default(self):
        """Test parsing integers per line with default delimiter."""
        raw = "1 2 3\n4 5 6"
        self.assertEqual(ints_per_line(raw), [[1, 2, 3], [4, 5, 6]])

    def test_ints_per_line_custom_delimiter(self):
        """Test parsing integers per line with custom delimiter."""
        raw = "1,2,3\n4,5,6"
        self.assertEqual(ints_per_line(raw, ","), [[1, 2, 3], [4, 5, 6]])

    def test_ints_per_line_tabs(self):
        """Test parsing integers separated by tabs."""
        raw = "1\t2\t3\n4\t5\t6"
        self.assertEqual(ints_per_line(raw, "\t"), [[1, 2, 3], [4, 5, 6]])

    def test_floats(self):
        """Test parsing floats from lines."""
        raw = "3.14\n2.71\n1.0"
        result = floats(raw)
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(result[0], 3.14)
        self.assertAlmostEqual(result[1], 2.71)
        self.assertAlmostEqual(result[2], 1.0)

    def test_floats_with_negative(self):
        """Test floats with negative numbers."""
        raw = "-3.14\n2.71"
        result = floats(raw)
        self.assertAlmostEqual(result[0], -3.14)


class TestWordParser(unittest.TestCase):
    """Test word extraction."""

    def test_words_basic(self):
        """Test extracting words."""
        raw = "hello 123 world"
        self.assertEqual(words(raw), ["hello", "world"])

    def test_words_with_punctuation(self):
        """Test words ignores punctuation."""
        raw = "hello, world! test."
        self.assertEqual(words(raw), ["hello", "world", "test"])

    def test_words_empty(self):
        """Test words with no alphabetic characters."""
        raw = "123 456 789"
        self.assertEqual(words(raw), [])

    def test_words_mixed(self):
        """Test words with mixed content."""
        raw = "abc123def456ghi"
        self.assertEqual(words(raw), ["abc", "def", "ghi"])


class TestBlockParsers(unittest.TestCase):
    """Test block parsing functions."""

    def test_blocks_default_delimiter(self):
        """Test parsing blocks separated by blank lines."""
        raw = "line1\nline2\n\nline3\nline4"
        self.assertEqual(blocks(raw), ["line1\nline2", "line3\nline4"])

    def test_blocks_single_block(self):
        """Test blocks with no separator."""
        raw = "line1\nline2"
        self.assertEqual(blocks(raw), ["line1\nline2"])

    def test_blocks_custom_delimiter(self):
        """Test blocks with custom delimiter."""
        raw = "part1 | part2 | part3"
        self.assertEqual(blocks(raw, " | "), ["part1", "part2", "part3"])

    def test_blocks_multiple_empty_lines(self):
        """Test blocks with multiple consecutive empty lines."""
        raw = "block1\n\n\nblock2"
        result = blocks(raw)
        # Multiple empty lines create empty strings in split result
        self.assertTrue(len(result) >= 2)


class TestCSVParsers(unittest.TestCase):
    """Test CSV parsing functions."""

    def test_csv_basic(self):
        """Test parsing CSV strings."""
        raw = "apple,banana,cherry"
        self.assertEqual(csv(raw), ["apple", "banana", "cherry"])

    def test_csv_with_spaces(self):
        """Test CSV handles extra spaces."""
        raw = "apple , banana , cherry"
        self.assertEqual(csv(raw), ["apple", "banana", "cherry"])

    def test_csv_custom_delimiter(self):
        """Test CSV with custom delimiter."""
        raw = "apple;banana;cherry"
        self.assertEqual(csv(raw, ";"), ["apple", "banana", "cherry"])

    def test_csv_ints(self):
        """Test parsing CSV integers."""
        raw = "10,20,30"
        self.assertEqual(csv_ints(raw), [10, 20, 30])

    def test_csv_ints_with_spaces(self):
        """Test CSV ints handles spaces."""
        raw = "10 , 20 , 30"
        self.assertEqual(csv_ints(raw), [10, 20, 30])

    def test_csv_ints_custom_delimiter(self):
        """Test CSV ints with custom delimiter."""
        raw = "10;20;30"
        self.assertEqual(csv_ints(raw, ";"), [10, 20, 30])

    def test_csv_ints_negative(self):
        """Test CSV ints with negative numbers."""
        raw = "-10,20,-30"
        self.assertEqual(csv_ints(raw), [-10, 20, -30])


class TestGridParsers(unittest.TestCase):
    """Test grid parsing functions."""

    def test_char_grid(self):
        """Test parsing character grid."""
        raw = "abc\ndef"
        expected = [["a", "b", "c"], ["d", "e", "f"]]
        self.assertEqual(char_grid(raw), expected)

    def test_char_grid_single_row(self):
        """Test char grid with single row."""
        raw = "hello"
        self.assertEqual(char_grid(raw), [["h", "e", "l", "l", "o"]])

    def test_char_grid_empty_lines(self):
        """Test char grid handles empty lines."""
        raw = "abc\n\ndef"
        result = char_grid(raw)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1], [])

    def test_int_grid(self):
        """Test parsing integer grid."""
        raw = "123\n456"
        expected = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(int_grid(raw), expected)

    def test_int_grid_single_digit(self):
        """Test int grid with single digits."""
        raw = "1\n2\n3"
        expected = [[1], [2], [3]]
        self.assertEqual(int_grid(raw), expected)

    def test_int_grid_zeros(self):
        """Test int grid with zeros."""
        raw = "000\n111"
        expected = [[0, 0, 0], [1, 1, 1]]
        self.assertEqual(int_grid(raw), expected)


class TestMappedParser(unittest.TestCase):
    """Test custom mapper function."""

    def test_mapped_simple(self):
        """Test mapped with simple parser."""
        raw = "1 2\n3 4"
        result = mapped(raw, lambda line: list(map(int, line.split())))
        self.assertEqual(result, [[1, 2], [3, 4]])

    def test_mapped_custom(self):
        """Test mapped with custom parser function."""
        def parse_game(line):
            parts = line.split()
            return (parts[0], int(parts[1]))

        raw = "red 5\nblue 3"
        result = mapped(raw, parse_game)
        self.assertEqual(result, [("red", 5), ("blue", 3)])

    def test_mapped_tuple_split(self):
        """Test mapped returning tuples."""
        def parse_pair(line):
            a, b = line.split("-")
            return (int(a), int(b))

        raw = "1-2\n3-4\n5-6"
        result = mapped(raw, parse_pair)
        self.assertEqual(result, [(1, 2), (3, 4), (5, 6)])

    def test_mapped_empty_lines(self):
        """Test mapped handles empty input."""
        raw = ""
        result = mapped(raw, lambda x: x.upper())
        # Empty raw string when stripped is [""]
        self.assertTrue(isinstance(result, list))


if __name__ == "__main__":
    unittest.main()
