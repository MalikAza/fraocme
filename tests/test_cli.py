import unittest
from unittest.mock import patch, MagicMock
import sys
from io import StringIO

from fraocme.cli import main, cmd_run, cmd_stats


class TestMainArgumentParsing(unittest.TestCase):
    """Test CLI argument parsing."""

    def test_main_with_no_arguments_prints_help(self):
        """Test main with no arguments prints help."""
        with patch('sys.argv', ['fraocme']):
            with patch('sys.exit') as mock_exit:
                with patch('sys.stdout', new=StringIO()):
                    main()
                    mock_exit.assert_called_once_with(0)

    def test_run_command_with_day(self):
        """Test run command with a specific day."""
        with patch('sys.argv', ['fraocme', 'run', '5']):
            with patch('fraocme.cli.cmd_run') as mock_run:
                main()
                mock_run.assert_called_once()

    def test_run_command_with_all_flag(self):
        """Test run command with --all flag."""
        with patch('sys.argv', ['fraocme', 'run', '--all']):
            with patch('fraocme.cli.cmd_run') as mock_run:
                main()
                mock_run.assert_called_once()

    def test_run_command_with_debug_flag(self):
        """Test run command with --debug flag."""
        with patch('sys.argv', ['fraocme', 'run', '1', '--debug']):
            with patch('fraocme.cli.cmd_run') as mock_run:
                main()
                args = mock_run.call_args[0][0]
                self.assertTrue(args.debug)

    def test_run_command_with_part_flag(self):
        """Test run command with --part flag."""
        with patch('sys.argv', ['fraocme', 'run', '1', '--part', '1']):
            with patch('fraocme.cli.cmd_run') as mock_run:
                main()
                args = mock_run.call_args[0][0]
                self.assertEqual(args.part, 1)

    def test_run_command_with_no_stats_flag(self):
        """Test run command with --no-stats flag."""
        with patch('sys.argv', ['fraocme', 'run', '1', '--no-stats']):
            with patch('fraocme.cli.cmd_run') as mock_run:
                main()
                args = mock_run.call_args[0][0]
                self.assertTrue(args.no_stats)

    def test_stats_command(self):
        """Test stats command."""
        with patch('sys.argv', ['fraocme', 'stats']):
            with patch('fraocme.cli.cmd_stats') as mock_stats:
                main()
                mock_stats.assert_called_once()

    def test_stats_command_with_day(self):
        """Test stats command with specific day."""
        with patch('sys.argv', ['fraocme', 'stats', '5']):
            with patch('fraocme.cli.cmd_stats') as mock_stats:
                main()
                args = mock_stats.call_args[0][0]
                self.assertEqual(args.day, 5)

    def test_stats_command_with_best_flag(self):
        """Test stats command with --best flag."""
        with patch('sys.argv', ['fraocme', 'stats', '--best']):
            with patch('fraocme.cli.cmd_stats') as mock_stats:
                main()
                args = mock_stats.call_args[0][0]
                self.assertTrue(args.best)


class TestCmdRun(unittest.TestCase):
    """Test cmd_run function."""

    @patch('fraocme.cli.Runner')
    @patch('fraocme.cli.Stats')
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

        cmd_run(args)
        
        mock_runner.run_all.assert_called_once_with(parts=[1, 2], debug=False)
        mock_stats.save.assert_called_once()

    @patch('fraocme.cli.Runner')
    @patch('fraocme.cli.Stats')
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

        cmd_run(args)
        
        mock_runner.day_exists.assert_called_once_with(5)
        mock_runner.run_day.assert_called_once_with(5, parts=[1, 2], debug=False)

    @patch('fraocme.cli.Runner')
    @patch('fraocme.cli.Stats')
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

        cmd_run(args)
        
        mock_runner.run_day.assert_called_once_with(5, parts=[1], debug=False)

    @patch('fraocme.cli.Runner')
    @patch('fraocme.cli.Stats')
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

        cmd_run(args)
        
        mock_stats.save.assert_not_called()

    @patch('fraocme.cli.Runner')
    @patch('fraocme.cli.Stats')
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

        with patch('sys.stdout', new=StringIO()):
            with self.assertRaises(SystemExit):
                cmd_run(args)

    @patch('fraocme.cli.Runner')
    @patch('fraocme.cli.Stats')
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

        with patch('sys.stdout', new=StringIO()):
            with self.assertRaises(SystemExit):
                cmd_run(args)


class TestCmdStats(unittest.TestCase):
    """Test cmd_stats function."""

    @patch('fraocme.cli.print_header')
    @patch('fraocme.cli.Stats')
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

    @patch('fraocme.cli.print_header')
    @patch('fraocme.cli.Stats')
    def test_cmd_stats_specific_day(self, mock_stats_class, mock_print_header):
        """Test stats command for specific day."""
        mock_stats = MagicMock()
        mock_stats_class.return_value = mock_stats

        args = MagicMock()
        args.day = 5
        args.best = False

        cmd_stats(args)
        
        mock_stats.print_day.assert_called_once_with(5, best_only=False)

    @patch('fraocme.cli.print_header')
    @patch('fraocme.cli.Stats')
    def test_cmd_stats_best_only(self, mock_stats_class, mock_print_header):
        """Test stats command with best_only flag."""
        mock_stats = MagicMock()
        mock_stats_class.return_value = mock_stats

        args = MagicMock()
        args.day = None
        args.best = True

        cmd_stats(args)
        
        mock_stats.print_all.assert_called_once_with(best_only=True)


if __name__ == '__main__':
    unittest.main()
