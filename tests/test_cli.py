import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

from fraocme.cli import cmd_create, cmd_run, cmd_stats, main


class TestMainArgumentParsing(unittest.TestCase):
    """Test CLI argument parsing."""

    def test_main_with_no_arguments_prints_help(self):
        """Test main with no arguments prints help."""
        with patch("sys.argv", ["fraocme"]):
            with patch("sys.exit") as mock_exit:
                with patch("sys.stdout", new=StringIO()):
                    main()
                    mock_exit.assert_called_once_with(0)

    def test_run_command_with_day(self):
        """Test run command with a specific day."""
        with patch("sys.argv", ["fraocme", "run", "5"]):
            with patch("fraocme.cli.cmd_run") as mock_run:
                main()
                mock_run.assert_called_once()

    def test_run_command_with_all_flag(self):
        """Test run command with --all flag."""
        with patch("sys.argv", ["fraocme", "run", "--all"]):
            with patch("fraocme.cli.cmd_run") as mock_run:
                main()
                mock_run.assert_called_once()

    def test_run_command_with_debug_flag(self):
        """Test run command with --debug flag."""
        with patch("sys.argv", ["fraocme", "run", "1", "--debug"]):
            with patch("fraocme.cli.cmd_run") as mock_run:
                main()
                args = mock_run.call_args[0][0]
                self.assertTrue(args.debug)

    def test_run_command_with_part_flag(self):
        """Test run command with --part flag."""
        with patch("sys.argv", ["fraocme", "run", "1", "--part", "1"]):
            with patch("fraocme.cli.cmd_run") as mock_run:
                main()
                args = mock_run.call_args[0][0]
                self.assertEqual(args.part, 1)

    def test_run_command_with_no_stats_flag(self):
        """Test run command with --no-stats flag."""
        with patch("sys.argv", ["fraocme", "run", "1", "--no-stats"]):
            with patch("fraocme.cli.cmd_run") as mock_run:
                main()
                args = mock_run.call_args[0][0]
                self.assertTrue(args.no_stats)

    def test_run_command_with_no_traceback_flag(self):
        """Test run command with --no-traceback flag."""
        with patch("sys.argv", ["fraocme", "run", "1", "--no-traceback"]):
            with patch("fraocme.cli.cmd_run") as mock_run:
                main()
                args = mock_run.call_args[0][0]
                self.assertTrue(args.no_traceback)

    def test_stats_command(self):
        """Test stats command."""
        with patch("sys.argv", ["fraocme", "stats"]):
            with patch("fraocme.cli.cmd_stats") as mock_stats:
                main()
                mock_stats.assert_called_once()

    def test_stats_command_with_day(self):
        """Test stats command with specific day."""
        with patch("sys.argv", ["fraocme", "stats", "5"]):
            with patch("fraocme.cli.cmd_stats") as mock_stats:
                main()
                args = mock_stats.call_args[0][0]
                self.assertEqual(args.day, 5)

    def test_stats_command_with_best_flag(self):
        """Test stats command with --best flag."""
        with patch("sys.argv", ["fraocme", "stats", "--best"]):
            with patch("fraocme.cli.cmd_stats") as mock_stats:
                main()
                args = mock_stats.call_args[0][0]
                self.assertTrue(args.best)


class TestCmdRun(unittest.TestCase):
    """Test cmd_run function."""

    @patch("fraocme.cli.Runner")
    @patch("fraocme.cli.Stats")
    def test_cmd_run_all_days(self, mock_stats_class, mock_runner_class):
        """Test running all days."""
        mock_runner = MagicMock()
        mock_stats = MagicMock()
        mock_runner_class.return_value = mock_runner
        mock_stats_class.return_value = mock_stats
        mock_runner.run_all.return_value = {1: {}, 2: {}}

        args = MagicMock()
        args.all = True
        args.part = None
        args.debug = False
        args.no_stats = False
        args.no_traceback = False

        cmd_run(args)

        mock_runner.run_all.assert_called_once_with(
            parts=[1, 2], debug=False, show_traceback=True
        )
        mock_stats.save.assert_called_once()

    @patch("fraocme.cli.Runner")
    @patch("fraocme.cli.Stats")
    def test_cmd_run_specific_day(self, mock_stats_class, mock_runner_class):
        """Test running specific day."""
        mock_runner = MagicMock()
        mock_stats = MagicMock()
        mock_runner_class.return_value = mock_runner
        mock_stats_class.return_value = mock_stats
        mock_runner.day_exists.return_value = True
        mock_runner.run_day.return_value = {}

        args = MagicMock()
        args.all = False
        args.day = 5
        args.part = None
        args.debug = False
        args.no_stats = False
        args.no_traceback = False

        cmd_run(args)

        mock_runner.day_exists.assert_called_once_with(5)
        mock_runner.run_day.assert_called_once_with(
            5, parts=[1, 2], debug=False, show_traceback=True
        )

    @patch("fraocme.cli.Runner")
    @patch("fraocme.cli.Stats")
    def test_cmd_run_specific_part(self, mock_stats_class, mock_runner_class):
        """Test running specific part."""
        mock_runner = MagicMock()
        mock_stats = MagicMock()
        mock_runner_class.return_value = mock_runner
        mock_stats_class.return_value = mock_stats
        mock_runner.day_exists.return_value = True
        mock_runner.run_day.return_value = {}

        args = MagicMock()
        args.all = False
        args.day = 5
        args.part = 1
        args.debug = False
        args.no_stats = False
        args.no_traceback = False

        cmd_run(args)

        mock_runner.run_day.assert_called_once_with(
            5, parts=[1], debug=False, show_traceback=True
        )

    @patch("fraocme.cli.Runner")
    @patch("fraocme.cli.Stats")
    def test_cmd_run_no_stats(self, mock_stats_class, mock_runner_class):
        """Test running without saving stats."""
        mock_runner = MagicMock()
        mock_stats = MagicMock()
        mock_runner_class.return_value = mock_runner
        mock_stats_class.return_value = mock_stats
        mock_runner.day_exists.return_value = True
        mock_runner.run_day.return_value = {}

        args = MagicMock()
        args.all = False
        args.day = 5
        args.part = None
        args.debug = False
        args.no_stats = True
        args.no_traceback = False

        cmd_run(args)

        mock_stats.save.assert_not_called()

    @patch("fraocme.cli.Runner")
    @patch("fraocme.cli.Stats")
    def test_cmd_run_day_not_exists(self, mock_stats_class, mock_runner_class):
        """Test running non-existent day."""
        mock_runner = MagicMock()
        mock_stats = MagicMock()
        mock_runner_class.return_value = mock_runner
        mock_stats_class.return_value = mock_stats
        mock_runner.day_exists.return_value = False

        args = MagicMock()
        args.all = False
        args.day = 999
        args.part = None
        args.debug = False
        args.no_stats = False
        args.no_traceback = False

        with patch("sys.stdout", new=StringIO()):
            with self.assertRaises(SystemExit):
                cmd_run(args)

    @patch("fraocme.cli.Runner")
    @patch("fraocme.cli.Stats")
    def test_cmd_run_no_day_specified(self, mock_stats_class, mock_runner_class):
        """Test running with no day specified and not --all."""
        mock_runner = MagicMock()
        mock_stats = MagicMock()
        mock_runner_class.return_value = mock_runner
        mock_stats_class.return_value = mock_stats

        args = MagicMock()
        args.all = False
        args.day = None
        args.part = None
        args.debug = False
        args.no_stats = False

        with patch("sys.stdout", new=StringIO()):
            with self.assertRaises(SystemExit):
                cmd_run(args)

    @patch("fraocme.cli.Runner")
    @patch("fraocme.cli.Stats")
    def test_cmd_run_with_no_traceback(self, mock_stats_class, mock_runner_class):
        """Test running with --no-traceback flag disables traceback."""
        mock_runner = MagicMock()
        mock_stats = MagicMock()
        mock_runner_class.return_value = mock_runner
        mock_stats_class.return_value = mock_stats
        mock_runner.day_exists.return_value = True
        mock_runner.run_day.return_value = {}

        args = MagicMock()
        args.all = False
        args.day = 5
        args.part = None
        args.debug = False
        args.no_stats = False
        args.no_traceback = True

        cmd_run(args)

        mock_runner.run_day.assert_called_once_with(
            5, parts=[1, 2], debug=False, show_traceback=False
        )


class TestCmdStats(unittest.TestCase):
    """Test cmd_stats function."""

    @patch("fraocme.cli.print_header")
    @patch("fraocme.cli.Stats")
    def test_cmd_stats_all(self, mock_stats_class, mock_print_header):
        """Test stats command for all days."""
        mock_stats = MagicMock()
        mock_stats_class.return_value = mock_stats

        args = MagicMock()
        args.day = None
        args.best = False

        cmd_stats(args)

        mock_print_header.assert_called_once()
        mock_stats.print_all.assert_called_once_with(best_only=False)

    @patch("fraocme.cli.print_header")
    @patch("fraocme.cli.Stats")
    def test_cmd_stats_specific_day(self, mock_stats_class, mock_print_header):
        """Test stats command for specific day."""
        mock_stats = MagicMock()
        mock_stats_class.return_value = mock_stats

        args = MagicMock()
        args.day = 5
        args.best = False

        cmd_stats(args)

        mock_stats.print_day.assert_called_once_with(5, best_only=False)

    @patch("fraocme.cli.print_header")
    @patch("fraocme.cli.Stats")
    def test_cmd_stats_best_only(self, mock_stats_class, mock_print_header):
        """Test stats command with best_only flag."""
        mock_stats = MagicMock()
        mock_stats_class.return_value = mock_stats

        args = MagicMock()
        args.day = None
        args.best = True

        cmd_stats(args)

        mock_stats.print_all.assert_called_once_with(best_only=True)


class TestCreateCommand(unittest.TestCase):
    """Test create command functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_day_dir = Path.cwd() / "days" / "day_12"
        # Clean up any existing test day
        if self.test_day_dir.exists():
            import shutil

            shutil.rmtree(self.test_day_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        if self.test_day_dir.exists():
            import shutil

            shutil.rmtree(self.test_day_dir)

    def test_create_command_creates_directory(self):
        """Test that create command creates the day directory."""
        args = MagicMock()
        args.day = 12

        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        self.assertTrue(self.test_day_dir.exists())

    def test_create_command_creates_input_file(self):
        """Test that create command creates input.txt file."""
        args = MagicMock()
        args.day = 12

        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        input_file = self.test_day_dir / "input.txt"
        self.assertTrue(input_file.exists())
        self.assertEqual(input_file.read_text(), "")

    def test_create_command_creates_solution_file(self):
        """Test that create command creates solution.py file."""
        args = MagicMock()
        args.day = 12

        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        solution_file = self.test_day_dir / "solution.py"
        self.assertTrue(solution_file.exists())

    def test_create_command_solution_contains_correct_class(self):
        """Test that solution.py contains correct class name."""
        args = MagicMock()
        args.day = 12

        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        solution_file = self.test_day_dir / "solution.py"
        content = solution_file.read_text()

        self.assertIn("class Day12(Solver):", content)
        init_sig = "def __init__(self, day: int = 12, debug: bool = False):"
        self.assertIn(init_sig, content)

    def test_create_command_solution_has_parse_method(self):
        """Test that solution.py contains parse method."""
        args = MagicMock()
        args.day = 12

        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        solution_file = self.test_day_dir / "solution.py"
        content = solution_file.read_text()

        self.assertIn("def parse(self, raw: str):", content)
        self.assertIn('return raw.strip().split("\\n")', content)

    def test_create_command_solution_has_part_methods(self):
        """Test that solution.py contains part1 and part2 methods."""
        args = MagicMock()
        args.day = 12

        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        solution_file = self.test_day_dir / "solution.py"
        content = solution_file.read_text()

        self.assertIn("def part1(self, data):", content)
        self.assertIn("def part2(self, data):", content)

    def test_create_command_solution_inherits_from_solver(self):
        """Test that solution.py imports and inherits from Solver."""
        args = MagicMock()
        args.day = 12

        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        solution_file = self.test_day_dir / "solution.py"
        content = solution_file.read_text()

        self.assertIn("from fraocme import Solver", content)
        self.assertIn("class Day12(Solver):", content)

    def test_create_command_warns_if_day_exists(self):
        """Test that create command warns if day already exists."""
        args = MagicMock()
        args.day = 12

        # Create the day first time
        with patch("sys.stdout", new=StringIO()):
            cmd_create(args)

        # Try to create again
        output = StringIO()
        with patch("sys.stdout", output):
            cmd_create(args)

        output_text = output.getvalue()
        self.assertIn("Warning:", output_text)
        self.assertIn("Day 12 already exists", output_text)

    def test_create_command_prints_success_message(self):
        """Test that create command prints success message."""
        args = MagicMock()
        args.day = 12

        output = StringIO()
        with patch("sys.stdout", output):
            cmd_create(args)

        output_text = output.getvalue()
        self.assertIn("Created day", output_text)
        self.assertIn("12", output_text)

    def test_create_command_prints_file_names(self):
        """Test that create command prints created file names."""
        args = MagicMock()
        args.day = 12

        output = StringIO()
        with patch("sys.stdout", output):
            cmd_create(args)

        output_text = output.getvalue()
        self.assertIn("input.txt", output_text)
        self.assertIn("solution.py", output_text)

    def test_create_command_different_day_numbers(self):
        """Test create command with different day numbers."""
        for day_num in [1, 5, 10, 25]:
            day_dir = Path.cwd() / "days" / f"day_{day_num:02d}"
            try:
                args = MagicMock()
                args.day = day_num

                with patch("sys.stdout", new=StringIO()):
                    cmd_create(args)

                self.assertTrue(day_dir.exists())
                solution_file = day_dir / "solution.py"
                content = solution_file.read_text()
                self.assertIn(f"class Day{day_num}(Solver):", content)
                self.assertIn(f"day: int = {day_num}", content)
            finally:
                # Clean up
                if day_dir.exists():
                    import shutil

                    shutil.rmtree(day_dir)

    def test_create_command_with_argv(self):
        """Test create command via command line arguments."""
        with patch("sys.argv", ["fraocme", "create", "98"]):
            with patch("fraocme.cli.cmd_create") as mock_create:
                main()
                mock_create.assert_called_once()
                args = mock_create.call_args[0][0]
                self.assertEqual(args.day, 98)

    def test_create_command_validates_day_range_lower_bound(self):
        """Test that create command rejects day 0."""
        args = MagicMock()
        args.day = 0

        output = StringIO()
        with patch("sys.stdout", output):
            with patch("sys.exit") as mock_exit:
                cmd_create(args)
                mock_exit.assert_called_once_with(1)

        output_text = output.getvalue()
        self.assertIn("Error:", output_text)
        self.assertIn("must be between 1 and 25", output_text)

    def test_create_command_validates_day_range_upper_bound(self):
        """Test that create command rejects day 26."""
        args = MagicMock()
        args.day = 26

        output = StringIO()
        with patch("sys.stdout", output):
            with patch("sys.exit") as mock_exit:
                cmd_create(args)
                mock_exit.assert_called_once_with(1)

        output_text = output.getvalue()
        self.assertIn("Error:", output_text)
        self.assertIn("must be between 1 and 25", output_text)

    def test_create_command_validates_negative_day(self):
        """Test that create command rejects negative day numbers."""
        args = MagicMock()
        args.day = -5

        output = StringIO()
        with patch("sys.stdout", output):
            with patch("sys.exit") as mock_exit:
                cmd_create(args)
                mock_exit.assert_called_once_with(1)

        output_text = output.getvalue()
        self.assertIn("Error:", output_text)

    def test_create_command_validates_large_day(self):
        """Test that create command rejects very large day numbers."""
        args = MagicMock()
        args.day = 100

        output = StringIO()
        with patch("sys.stdout", output):
            with patch("sys.exit") as mock_exit:
                cmd_create(args)
                mock_exit.assert_called_once_with(1)

        output_text = output.getvalue()
        self.assertIn("Error:", output_text)

    def test_create_command_accepts_valid_range(self):
        """Test that create command accepts all valid day numbers."""
        for day in [1, 5, 12, 24, 25]:
            day_dir = Path.cwd() / "days" / f"day_{day:02d}"
            try:
                args = MagicMock()
                args.day = day

                with patch("sys.stdout", new=StringIO()):
                    cmd_create(args)

                self.assertTrue(day_dir.exists())
            finally:
                # Clean up
                if day_dir.exists():
                    import shutil

                    shutil.rmtree(day_dir)

    def test_create_command_min_valid_day(self):
        """Test that create command accepts day 1."""
        test_day_dir = Path.cwd() / "days" / "day_01"
        try:
            args = MagicMock()
            args.day = 1

            with patch("sys.stdout", new=StringIO()):
                cmd_create(args)

            self.assertTrue(test_day_dir.exists())
            solution_file = test_day_dir / "solution.py"
            self.assertTrue(solution_file.exists())
        finally:
            if test_day_dir.exists():
                import shutil

                shutil.rmtree(test_day_dir)

    def test_create_command_max_valid_day(self):
        """Test that create command accepts day 25."""
        test_day_dir = Path.cwd() / "days" / "day_25"
        try:
            args = MagicMock()
            args.day = 25

            with patch("sys.stdout", new=StringIO()):
                cmd_create(args)

            self.assertTrue(test_day_dir.exists())
            solution_file = test_day_dir / "solution.py"
            self.assertTrue(solution_file.exists())
        finally:
            if test_day_dir.exists():
                import shutil

                shutil.rmtree(test_day_dir)


if __name__ == "__main__":
    unittest.main()
