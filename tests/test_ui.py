import sys
import unittest
from io import StringIO

from fraocme.ui.colors import Colors, c
from fraocme.ui.printer import print_header, print_section


class TestColors(unittest.TestCase):
    """Test Colors class constants."""

    def test_reset_code(self):
        """Test reset code exists."""
        self.assertEqual(Colors.RESET, "\033[0m")

    def test_regular_colors_exist(self):
        """Test regular color codes exist."""
        self.assertEqual(Colors.RED, "\033[31m")
        self.assertEqual(Colors.GREEN, "\033[32m")
        self.assertEqual(Colors.YELLOW, "\033[33m")
        self.assertEqual(Colors.MAGENTA, "\033[35m")
        self.assertEqual(Colors.CYAN, "\033[36m")

    def test_bright_colors_exist(self):
        """Test bright color codes exist."""
        self.assertEqual(Colors.BRIGHT_RED, "\033[91m")
        self.assertEqual(Colors.BRIGHT_GREEN, "\033[92m")
        self.assertEqual(Colors.BRIGHT_YELLOW, "\033[93m")
        self.assertEqual(Colors.BRIGHT_MAGENTA, "\033[95m")
        self.assertEqual(Colors.BRIGHT_CYAN, "\033[96m")

    def test_style_codes_exist(self):
        """Test style codes exist."""
        self.assertEqual(Colors.BOLD, "\033[1m")
        self.assertEqual(Colors.DIM, "\033[2m")


class TestColorHelper(unittest.TestCase):
    """Test c color helper class."""

    def test_wrap_format(self):
        """Test _wrap creates correct format."""
        result = c._wrap(Colors.RED, "text")
        expected = f"{Colors.RED}text{Colors.RESET}"
        self.assertEqual(result, expected)

    def test_red_color(self):
        """Test red color helper."""
        result = c.red("error")
        self.assertIn("error", result)
        self.assertIn(Colors.RED, result)
        self.assertIn(Colors.RESET, result)

    def test_green_color(self):
        """Test green color helper."""
        result = c.green("success")
        self.assertIn("success", result)
        self.assertIn(Colors.GREEN, result)
        self.assertIn(Colors.RESET, result)

    def test_yellow_color(self):
        """Test yellow color helper."""
        result = c.yellow("warning")
        self.assertIn("warning", result)
        self.assertIn(Colors.YELLOW, result)

    def test_cyan_color(self):
        """Test cyan color helper."""
        result = c.cyan("highlight")
        self.assertIn("highlight", result)
        self.assertIn(Colors.CYAN, result)

    def test_magenta_color(self):
        """Test magenta color helper."""
        result = c.magenta("text")
        self.assertIn("text", result)
        self.assertIn(Colors.MAGENTA, result)

    def test_bold_style(self):
        """Test bold style."""
        result = c.bold("important")
        self.assertIn("important", result)
        self.assertIn(Colors.BOLD, result)

    def test_dim_style(self):
        """Test dim style."""
        result = c.dim("muted")
        self.assertIn("muted", result)
        self.assertIn(Colors.DIM, result)

    def test_success_semantic(self):
        """Test success semantic color."""
        result = c.success("ok")
        self.assertIn("ok", result)
        self.assertIn(Colors.BRIGHT_GREEN, result)

    def test_error_semantic(self):
        """Test error semantic color."""
        result = c.error("failed")
        self.assertIn("failed", result)
        self.assertIn(Colors.BRIGHT_RED, result)

    def test_warning_semantic(self):
        """Test warning semantic color."""
        result = c.warning("alert")
        self.assertIn("alert", result)
        self.assertIn(Colors.BRIGHT_YELLOW, result)

    def test_info_semantic(self):
        """Test info semantic color."""
        result = c.info("note")
        self.assertIn("note", result)
        self.assertIn(Colors.BRIGHT_CYAN, result)

    def test_muted_semantic(self):
        """Test muted semantic color."""
        result = c.muted("quiet")
        self.assertIn("quiet", result)
        self.assertIn(Colors.DIM, result)

    def test_time_fast(self):
        """Test time formatting for fast execution."""
        result = c.time(50.0)
        self.assertIn("50.00ms", result)
        self.assertIn(Colors.BRIGHT_GREEN, result)

    def test_time_moderate(self):
        """Test time formatting for moderate execution."""
        result = c.time(500.0)
        self.assertIn("500.00ms", result)
        self.assertIn(Colors.BRIGHT_YELLOW, result)

    def test_time_slow(self):
        """Test time formatting for slow execution."""
        result = c.time(2000.0)
        self.assertIn("2000.00ms", result)
        self.assertIn(Colors.BRIGHT_RED, result)

    def test_nested_colors(self):
        """Test nesting color functions."""
        result = c.bold(c.green("text"))
        self.assertIn("text", result)
        self.assertIn(Colors.BOLD, result)
        self.assertIn(Colors.GREEN, result)


class TestPrinter(unittest.TestCase):
    """Test printer functions."""

    def test_print_header_default_width(self):
        """Test print_header with default width."""
        captured_output = StringIO()
        sys.stdout = captured_output
        print_header("Test Header")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Test Header", output)
        self.assertIn("❄", output)
        self.assertIn("🎄", output)

    def test_print_header_custom_width(self):
        """Test print_header with custom width."""
        captured_output = StringIO()
        sys.stdout = captured_output
        print_header("Test", width=20)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Test", output)
        self.assertIn("❄", output)

    def test_print_section_default_width(self):
        """Test print_section with default width."""
        captured_output = StringIO()
        sys.stdout = captured_output
        print_section("Test Section")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Test Section", output)
        self.assertIn("⭐", output)

    def test_print_section_custom_width(self):
        """Test print_section with custom width."""
        captured_output = StringIO()
        sys.stdout = captured_output
        print_section("Test", width=30)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Test", output)
        self.assertIn("⭐", output)

    def test_print_header_structure(self):
        """Test print_header has correct structure."""
        captured_output = StringIO()
        sys.stdout = captured_output
        print_header("Title")
        sys.stdout = sys.__stdout__

        lines = captured_output.getvalue().strip().split("\n")
        self.assertTrue(lines[0].startswith("❄"))
        self.assertIn("Title", lines[1])
        self.assertTrue(lines[2].startswith("❄"))

    def test_print_section_structure(self):
        """Test print_section has correct structure."""
        captured_output = StringIO()
        sys.stdout = captured_output
        print_section("Section")
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Section", output)
        self.assertIn("⭐", output)


if __name__ == "__main__":
    unittest.main()
