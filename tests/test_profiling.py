import unittest
import time
import json
import tempfile
import shutil
from pathlib import Path
from io import StringIO
import sys

from fraocme.profiling import Timer, Stats, timed, benchmark


class TestTimer(unittest.TestCase):
    """Test Timer class for benchmarking."""

    def test_timer_initialization(self):
        """Test timer initializes correctly."""
        timer = Timer()
        self.assertIsNone(timer._start)
        self.assertEqual(timer.laps, [])

    def test_timer_start_returns_self(self):
        """Test start returns self for chaining."""
        timer = Timer()
        result = timer.start()
        self.assertIs(result, timer)

    def test_timer_stop_returns_elapsed(self):
        """Test stop returns elapsed time."""
        timer = Timer().start()
        time.sleep(0.01)  # Sleep for 10ms
        elapsed = timer.stop()
        
        self.assertIsInstance(elapsed, float)
        self.assertGreaterEqual(elapsed, 10)  # At least 10ms

    def test_timer_stop_without_start(self):
        """Test stop raises error if not started."""
        timer = Timer()
        with self.assertRaises(RuntimeError):
            timer.stop()

    def test_timer_lap(self):
        """Test lap returns current time without stopping."""
        timer = Timer().start()
        time.sleep(0.01)
        
        lap = timer.lap()
        self.assertGreaterEqual(lap, 10)
        
        # Timer should still be running
        lap2 = timer.lap()
        self.assertGreaterEqual(lap2, lap)

    def test_timer_lap_without_start(self):
        """Test lap raises error if not started."""
        timer = Timer()
        with self.assertRaises(RuntimeError):
            timer.lap()

    def test_timer_reset_returns_self(self):
        """Test reset returns self for chaining."""
        timer = Timer()
        result = timer.reset()
        self.assertIs(result, timer)

    def test_timer_reset_clears_laps(self):
        """Test reset clears lap history."""
        timer = Timer().start()
        timer.stop()
        timer.reset()
        
        self.assertEqual(timer.laps, [])
        self.assertIsNone(timer._start)

    def test_timer_laps_property(self):
        """Test laps property returns copy."""
        timer = Timer().start()
        timer.stop()
        
        laps1 = timer.laps
        laps2 = timer.laps
        
        self.assertEqual(laps1, laps2)
        self.assertIsNot(laps1, laps2)  # Different list objects

    def test_timer_total(self):
        """Test total sums all laps."""
        timer = Timer()
        timer.start()
        time.sleep(0.005)
        timer.stop()
        
        timer.start()
        time.sleep(0.005)
        timer.stop()
        
        total = timer.total
        self.assertGreaterEqual(total, 10)  # At least 10ms total

    def test_timer_total_empty(self):
        """Test total returns 0 with no laps."""
        timer = Timer()
        self.assertEqual(timer.total, 0.0)

    def test_timer_average(self):
        """Test average calculates mean."""
        timer = Timer()
        
        timer.start()
        timer.stop()
        timer.start()
        timer.stop()
        
        avg = timer.average
        total = timer.total
        
        self.assertAlmostEqual(avg, total / 2)

    def test_timer_average_empty(self):
        """Test average returns 0 with no laps."""
        timer = Timer()
        self.assertEqual(timer.average, 0.0)

    def test_timer_min(self):
        """Test min finds minimum lap."""
        timer = Timer()
        
        timer.start()
        time.sleep(0.002)
        timer.stop()
        
        timer.start()
        time.sleep(0.01)  # Longer
        timer.stop()
        
        min_lap = timer.min
        self.assertTrue(0 < min_lap < 5)

    def test_timer_min_empty(self):
        """Test min returns 0 with no laps."""
        timer = Timer()
        self.assertEqual(timer.min, 0.0)

    def test_timer_max(self):
        """Test max finds maximum lap."""
        timer = Timer()
        
        timer.start()
        time.sleep(0.002)
        timer.stop()
        
        timer.start()
        time.sleep(0.01)
        timer.stop()
        
        max_lap = timer.max
        self.assertGreaterEqual(max_lap, 10)

    def test_timer_max_empty(self):
        """Test max returns 0 with no laps."""
        timer = Timer()
        self.assertEqual(timer.max, 0.0)

    def test_timer_chaining(self):
        """Test method chaining."""
        timer = Timer()
        result = timer.reset().start()
        
        time.sleep(0.005)
        timer.stop()
        
        self.assertGreater(timer.total, 0)


class TestTimedDecorator(unittest.TestCase):
    """Test timed decorator."""

    def test_timed_decorator_preserves_function(self):
        """Test timed decorator preserves function name."""
        @timed
        def my_func():
            return 42
        
        self.assertEqual(my_func.__name__, "my_func")

    def test_timed_decorator_returns_result(self):
        """Test timed decorator returns function result."""
        @timed
        def add(a, b):
            return a + b
        
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_timed_decorator_prints_output(self):
        """Test timed decorator prints timing."""
        @timed
        def sleep_short():
            time.sleep(0.01)
            return "done"
        
        captured = StringIO()
        sys.stdout = captured
        
        result = sleep_short()
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertEqual(result, "done")
        self.assertIn("sleep_short", output)
        self.assertIn("ms", output)


class TestBenchmarkDecorator(unittest.TestCase):
    """Test benchmark decorator."""

    def test_benchmark_decorator_returns_result(self):
        """Test benchmark decorator returns function result."""
        @benchmark(iterations=2)
        def add(a, b):
            return a + b
        
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_benchmark_decorator_prints_output(self):
        """Test benchmark decorator prints stats."""
        @benchmark(iterations=3)
        def noop():
            return 42
        
        captured = StringIO()
        sys.stdout = captured
        
        noop()
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("noop", output)
        self.assertIn("3 runs", output)
        self.assertIn("avg", output)
        self.assertIn("min", output)
        self.assertIn("max", output)


class TestStats(unittest.TestCase):
    """Test Stats class for tracking statistics."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.stats_file = Path(self.temp_dir) / "stats.json"

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_stats_initialization(self):
        """Test Stats initializes correctly."""
        stats = Stats(path=self.stats_file)
        self.assertEqual(stats.path, self.stats_file)
        self.assertEqual(stats._data, {})

    def test_stats_initialization_loads_existing(self):
        """Test Stats loads existing file."""
        data = {"day_01": {"part1": {"answer": 42}}}
        self.stats_file.write_text(json.dumps(data))
        
        stats = Stats(path=self.stats_file)
        self.assertEqual(stats._data, data)

    def test_stats_save(self):
        """Test Stats saves to file."""
        stats = Stats(path=self.stats_file)
        stats._data = {"day_01": {"part1": {"answer": 42}}}
        stats.save()
        
        content = json.loads(self.stats_file.read_text())
        self.assertEqual(content, stats._data)

    def test_stats_update_new_entry(self):
        """Test Stats creates new day entry."""
        stats = Stats(path=self.stats_file)
        results = {1: (42, 100.5), 2: (99, 200.3)}
        
        stats.update(1, results)
        
        day_data = stats.get_day(1)
        self.assertIsNotNone(day_data)
        self.assertEqual(day_data["part1"]["answer"], 42)
        self.assertEqual(day_data["part2"]["answer"], 99)

    def test_stats_update_increments_runs(self):
        """Test Stats increments run counter."""
        stats = Stats(path=self.stats_file)
        
        stats.update(1, {1: (42, 100.0)})
        stats.update(1, {1: (42, 105.0)})
        
        day_data = stats.get_day(1)
        self.assertEqual(day_data["part1"]["runs"], 2)

    def test_stats_update_tracks_min(self):
        """Test Stats tracks minimum time."""
        stats = Stats(path=self.stats_file)
        
        stats.update(1, {1: (42, 100.0)})
        stats.update(1, {1: (42, 50.0)})
        stats.update(1, {1: (42, 75.0)})
        
        day_data = stats.get_day(1)
        self.assertEqual(day_data["part1"]["min_ms"], 50.0)

    def test_stats_get_day_not_found(self):
        """Test Stats get_day returns None for missing day."""
        stats = Stats(path=self.stats_file)
        self.assertIsNone(stats.get_day(999))

    def test_stats_get_all(self):
        """Test Stats get_all returns copy."""
        stats = Stats(path=self.stats_file)
        stats._data = {"day_01": {"part1": {"answer": 42}}}
        
        all_data = stats.get_all()
        self.assertEqual(all_data, stats._data)
        self.assertIsNot(all_data, stats._data)

    def test_stats_print_day(self):
        """Test Stats print_day function."""
        stats = Stats(path=self.stats_file)
        results = {1: (42, 100.0)}
        stats.update(1, results)
        
        captured = StringIO()
        sys.stdout = captured
        
        stats.print_day(1)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("Day 1", output)
        self.assertIn("42", output)

    def test_stats_print_day_no_stats(self):
        """Test Stats print_day with missing day."""
        stats = Stats(path=self.stats_file)
        
        captured = StringIO()
        sys.stdout = captured
        
        stats.print_day(999)
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("No stats", output)

    def test_stats_print_all_empty(self):
        """Test Stats print_all with no data."""
        stats = Stats(path=self.stats_file)
        
        captured = StringIO()
        sys.stdout = captured
        
        stats.print_all()
        
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
        self.assertIn("No stats", output)

    def test_stats_default_path(self):
        """Test Stats uses default path."""
        stats = Stats()
        self.assertEqual(stats.path, Path.cwd() / "stats.json")


if __name__ == "__main__":
    unittest.main()
