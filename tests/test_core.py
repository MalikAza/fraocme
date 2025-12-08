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


if __name__ == "__main__":
    unittest.main()
