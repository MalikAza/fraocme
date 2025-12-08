import shutil
import tempfile
import unittest
from pathlib import Path

from fraocme.core import Runner, Solver


class DummySolver(Solver):
    """Concrete implementation of Solver for testing."""

    def parse(self, raw: str):
        return raw.strip().split("\n")

    def part1(self, data):
        return len(data)

    def part2(self, data):
        return sum(len(line) for line in data)


class TestSolver(unittest.TestCase):
    """Test Solver base class."""

    def setUp(self):
        """Set up test fixtures."""
        self.solver = DummySolver(day=1, debug=False)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_solver_initialization(self):
        """Test solver initializes with correct attributes."""
        solver = DummySolver(day=5, debug=True)
        self.assertEqual(solver.day, 5)
        self.assertTrue(solver.debug_enabled)

    def test_solver_show_traceback_default(self):
        """Test solver shows traceback by default."""
        solver = DummySolver(day=1)
        self.assertTrue(solver.show_traceback)

    def test_solver_show_traceback_disabled(self):
        """Test solver can disable traceback display."""
        solver = DummySolver(day=1, show_traceback=False)
        self.assertFalse(solver.show_traceback)

    def test_solver_copy_input_default(self):
        """Test solver copies input by default."""
        solver = DummySolver(day=1)
        self.assertTrue(solver.copy_input)

    def test_solver_copy_input_disabled(self):
        """Test solver can disable input copying."""
        solver = DummySolver(day=1, copy_input=False)
        self.assertFalse(solver.copy_input)

    def test_set_input_dir(self):
        """Test setting input directory."""
        path = Path(self.temp_dir)
        result = self.solver.set_input_dir(path)

        self.assertEqual(self.solver._input_dir, path)
        self.assertIs(result, self.solver)  # Returns self for chaining

    def test_set_input_dir_chaining(self):
        """Test set_input_dir returns self for method chaining."""
        path = Path(self.temp_dir)
        result = self.solver.set_input_dir(path)
        self.assertIs(result, self.solver)

    def test_load_without_input_dir(self):
        """Test load raises error when input dir not set."""
        with self.assertRaises(ValueError):
            self.solver.load()

    def test_load_missing_input_file(self):
        """Test load raises error when input.txt doesn't exist."""
        self.solver.set_input_dir(Path(self.temp_dir))

        with self.assertRaises(FileNotFoundError):
            self.solver.load()

    def test_load_parses_input(self):
        """Test load correctly parses input."""
        input_file = Path(self.temp_dir) / "input.txt"
        input_file.write_text("line1\nline2\nline3")

        self.solver.set_input_dir(Path(self.temp_dir))
        data = self.solver.load()

        self.assertEqual(data, ["line1", "line2", "line3"])

    def test_load_strips_whitespace(self):
        """Test load strips leading/trailing whitespace."""
        input_file = Path(self.temp_dir) / "input.txt"
        input_file.write_text("  line1\nline2  \n")

        self.solver.set_input_dir(Path(self.temp_dir))
        data = self.solver.load()

        self.assertEqual(data, ["line1", "line2"])

    def test_load_with_copy_input_true(self):
        """Test load creates copy when copy_input is True."""
        solver = DummySolver(day=1, copy_input=True)
        input_file = Path(self.temp_dir) / "input.txt"
        input_file.write_text("line1\nline2")

        solver.set_input_dir(Path(self.temp_dir))
        data1 = solver.load()
        data2 = solver.load()

        # Different list objects (due to deepcopy)
        self.assertIsNot(data1, data2)

    def test_parse_abstract(self):
        """Test that parse is abstract."""
        with self.assertRaises(TypeError):
            Solver(day=1)

    def test_part1_abstract(self):
        """Test that part1 is abstract."""
        with self.assertRaises(TypeError):
            Solver(day=1)

    def test_part2_abstract(self):
        """Test that part2 is abstract."""
        with self.assertRaises(TypeError):
            Solver(day=1)

    def test_run_method_success(self):
        """Test run method executes both parts successfully."""
        import io
        from contextlib import redirect_stdout

        input_file = Path(self.temp_dir) / "input.txt"
        input_file.write_text("line1\nline2\nline3")
        self.solver.set_input_dir(Path(self.temp_dir))

        # Capture output
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            results = self.solver.run([1, 2])

        output = captured_output.getvalue()

        # Check that both parts ran
        self.assertIn("Part", output)
        self.assertEqual(len(results), 2)
        self.assertIn(1, results)
        self.assertIn(2, results)

        # Check results format (answer, elapsed_ms)
        self.assertEqual(results[1][0], 3)  # part1 returns len(data)
        self.assertEqual(results[2][0], 15)  # part2 returns sum of lengths
        self.assertIsInstance(results[1][1], float)
        self.assertIsInstance(results[2][1], float)

    def test_run_method_single_part(self):
        """Test run method with single part."""
        import io
        from contextlib import redirect_stdout

        input_file = Path(self.temp_dir) / "input.txt"
        input_file.write_text("line1\nline2")
        self.solver.set_input_dir(Path(self.temp_dir))

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            results = self.solver.run([1])

        self.assertEqual(len(results), 1)
        self.assertIn(1, results)
        self.assertNotIn(2, results)

    def test_run_method_with_error(self):
        """Test run method handles errors gracefully."""
        import io
        from contextlib import redirect_stdout

        class ErrorSolver(Solver):
            def parse(self, raw):
                return raw

            def part1(self, data):
                raise ValueError("Test error")

            def part2(self, data):
                return 42

        solver = ErrorSolver(day=1, show_traceback=False)
        input_file = Path(self.temp_dir) / "input.txt"
        input_file.write_text("test")
        solver.set_input_dir(Path(self.temp_dir))

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            results = solver.run([1])

        output = captured_output.getvalue()

        # Check error was handled
        self.assertIn("ERROR", output)
        self.assertEqual(results[1][0], None)
        self.assertEqual(results[1][1], 0.0)

    def test_run_method_with_traceback(self):
        """Test run method shows traceback when enabled."""
        import io

        class ErrorSolver(Solver):
            def parse(self, raw):
                return raw

            def part1(self, data):
                raise ValueError("Test error")

            def part2(self, data):
                return 42

        solver = ErrorSolver(day=1, show_traceback=True)
        input_file = Path(self.temp_dir) / "input.txt"
        input_file.write_text("test")
        solver.set_input_dir(Path(self.temp_dir))

        # Capture stdout while running to ensure traceback is printed
        captured_output = io.StringIO()
        from contextlib import redirect_stdout

        with redirect_stdout(captured_output):
            solver.run([1])

        output = captured_output.getvalue()

        # Check traceback is shown
        self.assertIn("Traceback", output)
        self.assertIn("ValueError", output)

    def test_debug_disabled(self):
        """Test debug method does nothing when debug is disabled."""
        import io
        from contextlib import redirect_stdout

        solver = DummySolver(day=1, debug=False)

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            solver.debug("This should not print")

        self.assertEqual(captured_output.getvalue(), "")

    def test_debug_enabled(self):
        """Test debug method prints when debug is enabled."""
        import io
        from contextlib import redirect_stdout

        solver = DummySolver(day=1, debug=True)

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            solver.debug("Debug message")

        self.assertIn("Debug message", captured_output.getvalue())

    def test_debug_with_callable(self):
        """Test debug method handles callable arguments."""
        import io
        from contextlib import redirect_stdout

        solver = DummySolver(day=1, debug=True)

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            solver.debug(lambda: "Callable result")

        self.assertIn("Callable result", captured_output.getvalue())

    def test_debug_with_callable_returning_none(self):
        """Test debug method handles callable returning None."""
        import io
        from contextlib import redirect_stdout

        solver = DummySolver(day=1, debug=True)

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            solver.debug(lambda: None)

        # Should not print anything for None result
        self.assertEqual(captured_output.getvalue().strip(), "")

    def test_debug_with_callable_raising_exception(self):
        """Test debug method handles callable that raises exception."""
        import io
        from contextlib import redirect_stdout

        solver = DummySolver(day=1, debug=True)

        def error_func():
            raise ValueError("Test error")

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            solver.debug(error_func)

        output = captured_output.getvalue()
        self.assertIn("debug callable raised", output)
        self.assertIn("Test error", output)


class TestRunner(unittest.TestCase):
    """Test Runner class for discovering and running solvers."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.base_dir = Path(self.temp_dir) / "days"
        self.runner = Runner(base_dir=self.base_dir)

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_runner_initialization_default(self):
        """Test Runner uses current working directory by default."""
        runner = Runner()
        self.assertEqual(runner.base_dir, Path.cwd() / "days")

    def test_runner_initialization_custom(self):
        """Test Runner with custom base directory."""
        custom_dir = Path("/custom/path")
        runner = Runner(base_dir=custom_dir)
        self.assertEqual(runner.base_dir, custom_dir)

    def test_get_day_dir(self):
        """Test getting directory for a specific day."""
        day_dir = self.runner.get_day_dir(5)
        expected = self.base_dir / "day_05"
        self.assertEqual(day_dir, expected)

    def test_get_day_dir_zero_padded(self):
        """Test day directories are zero-padded."""
        day1 = self.runner.get_day_dir(1)
        day10 = self.runner.get_day_dir(10)

        self.assertTrue(str(day1).endswith("day_01"))
        self.assertTrue(str(day10).endswith("day_10"))

    def test_day_exists_false(self):
        """Test day_exists returns False for non-existent days."""
        self.assertFalse(self.runner.day_exists(1))

    def test_day_exists_true(self):
        """Test day_exists returns True for existing days."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)
        solution_file = day_dir / "solution.py"
        solution_file.write_text("# test")

        self.assertTrue(self.runner.day_exists(1))

    def test_get_all_days_empty(self):
        """Test get_all_days returns empty list when no days exist."""
        self.assertEqual(self.runner.get_all_days(), [])

    def test_get_all_days_no_base_dir(self):
        """Test get_all_days handles missing base directory."""
        runner = Runner(base_dir=Path("/nonexistent"))
        self.assertEqual(runner.get_all_days(), [])

    def test_get_all_days_multiple(self):
        """Test get_all_days returns sorted list of available days."""
        # Create day 1, 3, 2
        for day in [1, 3, 2]:
            day_dir = self.runner.get_day_dir(day)
            day_dir.mkdir(parents=True)
            (day_dir / "solution.py").write_text("# test")

        days = self.runner.get_all_days()
        self.assertEqual(days, [1, 2, 3])

    def test_get_all_days_ignores_no_solution(self):
        """Test get_all_days ignores days without solution.py."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)
        # No solution.py created

        self.assertEqual(self.runner.get_all_days(), [])

    def test_get_all_days_ignores_invalid_dirs(self):
        """Test get_all_days ignores invalid directory names."""
        self.base_dir.mkdir(parents=True)
        invalid_dir = self.base_dir / "invalid_name"
        invalid_dir.mkdir()
        (invalid_dir / "solution.py").write_text("# test")

        self.assertEqual(self.runner.get_all_days(), [])

    def test_load_solver_not_found(self):
        """Test load_solver raises error for non-existent day."""
        with self.assertRaises(FileNotFoundError):
            self.runner.load_solver(1)

    def test_load_solver_success(self):
        """Test load_solver successfully loads a solver."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        # Create a simple solver
        solution_code = """
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw):
        return raw.strip()

    def part1(self, data):
        return 42

    def part2(self, data):
        return 99
"""
        (day_dir / "solution.py").write_text(solution_code)
        (day_dir / "input.txt").write_text("test input")

        solver = self.runner.load_solver(1)

        self.assertIsInstance(solver, Solver)
        self.assertEqual(solver.day, 1)
        self.assertEqual(solver._input_dir, day_dir)

    def test_load_solver_with_debug(self):
        """Test load_solver respects debug flag."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        solution_code = """
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): return raw.strip()
    def part1(self, data): return 42
    def part2(self, data): return 99
"""
        (day_dir / "solution.py").write_text(solution_code)

        solver = self.runner.load_solver(1, debug=True)
        self.assertTrue(solver.debug_enabled)

    def test_load_solver_with_show_traceback_default(self):
        """Test load_solver shows traceback by default."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        solution_code = """
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): return raw.strip()
    def part1(self, data): return 42
    def part2(self, data): return 99
"""
        (day_dir / "solution.py").write_text(solution_code)

        solver = self.runner.load_solver(1)
        self.assertTrue(solver.show_traceback)

    def test_load_solver_with_show_traceback_disabled(self):
        """Test load_solver respects show_traceback flag."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        solution_code = """
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): return raw.strip()
    def part1(self, data): return 42
    def part2(self, data): return 99
"""
        (day_dir / "solution.py").write_text(solution_code)

        solver = self.runner.load_solver(1, show_traceback=False)
        self.assertFalse(solver.show_traceback)

    def test_load_solver_no_solver_class(self):
        """Test load_solver raises error if no Solver subclass found."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        # File with no Solver subclass
        (day_dir / "solution.py").write_text("x = 42")

        with self.assertRaises(ValueError):
            self.runner.load_solver(1)

    def test_load_solver_with_import_error(self):
        """Test load_solver handles module loading errors."""
        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        # Create a solution file with syntax error
        (day_dir / "solution.py").write_text("this is not valid python syntax {{")

        with self.assertRaises(Exception):
            self.runner.load_solver(1)

    def test_run_day_success(self):
        """Test run_day executes a day successfully."""
        import io
        from contextlib import redirect_stdout

        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        solution_code = """
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): return raw.strip()
    def part1(self, data): return 42
    def part2(self, data): return 99
"""
        (day_dir / "solution.py").write_text(solution_code)
        (day_dir / "input.txt").write_text("test input")

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            results = self.runner.run_day(1)

        self.assertEqual(results[1][0], 42)
        self.assertEqual(results[2][0], 99)

    def test_run_day_with_parts_filter(self):
        """Test run_day with specific parts."""
        import io
        from contextlib import redirect_stdout

        day_dir = self.runner.get_day_dir(1)
        day_dir.mkdir(parents=True)

        solution_code = """
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): return raw.strip()
    def part1(self, data): return 42
    def part2(self, data): return 99
"""
        (day_dir / "solution.py").write_text(solution_code)
        (day_dir / "input.txt").write_text("test input")

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            results = self.runner.run_day(1, parts=[1])

        self.assertEqual(len(results), 1)
        self.assertIn(1, results)
        self.assertNotIn(2, results)

    def test_run_all_with_multiple_days(self):
        """Test run_all executes all available days."""
        import io
        from contextlib import redirect_stdout

        solution_code = """
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): return raw.strip()
    def part1(self, data): return 42
    def part2(self, data): return 99
"""

        # Create days 1 and 2
        for day in [1, 2]:
            day_dir = self.runner.get_day_dir(day)
            day_dir.mkdir(parents=True)
            (day_dir / "solution.py").write_text(solution_code)
            (day_dir / "input.txt").write_text("test")

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            results = self.runner.run_all()

        self.assertEqual(len(results), 2)
        self.assertIn(1, results)
        self.assertIn(2, results)

    def test_run_all_handles_errors(self):
        """Test run_all continues on error."""
        import io
        from contextlib import redirect_stdout

        # Day 1 - works
        day1_dir = self.runner.get_day_dir(1)
        day1_dir.mkdir(parents=True)
        (day1_dir / "solution.py").write_text("""
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): return raw.strip()
    def part1(self, data): return 42
    def part2(self, data): return 99
""")
        (day1_dir / "input.txt").write_text("test")

        # Day 2 - has error
        day2_dir = self.runner.get_day_dir(2)
        day2_dir.mkdir(parents=True)
        (day2_dir / "solution.py").write_text("""
from fraocme.core import Solver

class DaySolver(Solver):
    def parse(self, raw): raise ValueError("Parse error")
    def part1(self, data): return 42
    def part2(self, data): return 99
""")
        (day2_dir / "input.txt").write_text("test")

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            results = self.runner.run_all()

        # Day 1 should succeed
        self.assertIn(1, results)
        # Day 2 should fail but not crash: solver prints error details
        output = captured_output.getvalue()
        # Expect the solver error output (ERROR and Traceback)
        self.assertIn("ERROR - Parse error", output)
        self.assertIn("Traceback", output)


if __name__ == "__main__":
    unittest.main()
