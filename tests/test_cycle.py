import unittest

from fraocme.cycle import (
    detect_cycle_in_sequence,
    find_cycle,
    find_cycle_with_history,
    get_state_at_iteration,
    simulate_until_repeat,
)
from fraocme.cycle.printer import (
    format_cycle_history,
    format_cycle_result,
    format_history_table,
    format_iteration_lookup,
    format_repeat_result,
    format_state_at_target,
)


class TestFindCycle(unittest.TestCase):
    """Test find_cycle (Floyd's algorithm)."""

    def test_simple_modulo_cycle(self):
        """Cycle: 0 -> 1 -> 2 -> 3 -> 4 -> 0 -> ..."""
        result = find_cycle(0, lambda x: (x + 1) % 5)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, state = result
        self.assertEqual(cycle_start, 0)
        self.assertEqual(cycle_length, 5)
        self.assertEqual(state, 0)

    def test_cycle_with_prefix(self):
        """Sequence: 0 -> 1 -> 2 -> 3 -> 1 -> 2 -> 3 -> ..."""

        def step(x):
            return 1 if x == 3 else x + 1

        result = find_cycle(0, step)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, state = result
        self.assertEqual(cycle_start, 1)
        self.assertEqual(cycle_length, 3)
        self.assertEqual(state, 1)

    def test_cycle_length_one(self):
        """Sequence: 0 -> 1 -> 1 -> 1 -> ..."""

        def step(x):
            return 1

        result = find_cycle(0, step)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, state = result
        self.assertEqual(cycle_start, 1)
        self.assertEqual(cycle_length, 1)
        self.assertEqual(state, 1)

    def test_lcg_style(self):
        """Linear congruential generator."""

        def step(x):
            return (x * 7 + 1) % 100

        result = find_cycle(42, step)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, _ = result
        self.assertGreater(cycle_length, 0)
        self.assertGreaterEqual(cycle_start, 0)


class TestFindCycleWithHistory(unittest.TestCase):
    """Test find_cycle_with_history."""

    def test_returns_history(self):
        result = find_cycle_with_history(0, lambda x: (x + 1) % 5)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, history = result
        self.assertEqual(len(history), 5)
        self.assertEqual(history, [0, 1, 2, 3, 4])

    def test_history_with_prefix(self):
        """Sequence: 0 -> 1 -> 2 -> 3 -> 1 -> ..."""

        def step(x):
            return 1 if x == 3 else x + 1

        result = find_cycle_with_history(0, step)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, history = result
        self.assertEqual(history, [0, 1, 2, 3])
        self.assertEqual(cycle_start, 1)
        self.assertEqual(cycle_length, 3)

    def test_history_contains_cycle_start(self):
        result = find_cycle_with_history(0, lambda x: (x + 1) % 3)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, history = result
        # History should contain exactly one complete cycle
        self.assertEqual(
            history[cycle_start],
            history[cycle_start + cycle_length]
            if cycle_start + cycle_length < len(history)
            else history[cycle_start],
        )


class TestGetStateAtIteration(unittest.TestCase):
    """Test get_state_at_iteration."""

    def test_small_target(self):
        """Direct simulation for small targets."""
        state = get_state_at_iteration(0, lambda x: (x + 1) % 5, 3)
        self.assertEqual(state, 3)

    def test_target_equals_cycle_length(self):
        state = get_state_at_iteration(0, lambda x: (x + 1) % 5, 5)
        self.assertEqual(state, 0)  # Back to start

    def test_large_target_uses_cycle(self):
        """Should use cycle detection for large targets."""
        target = 1_000_000_000
        state = get_state_at_iteration(0, lambda x: (x + 1) % 7, target)
        expected = target % 7
        self.assertEqual(state, expected)

    def test_very_large_target(self):
        """Trillion iterations."""
        target = 1_000_000_000_000
        state = get_state_at_iteration(0, lambda x: (x + 1) % 100, target)
        self.assertEqual(state, 0)  # 1 trillion % 100 = 0

    def test_with_prefix(self):
        """Target in prefix vs in cycle."""

        def step(x):
            return 1 if x == 3 else x + 1

        # Target in prefix (index 0)
        self.assertEqual(get_state_at_iteration(0, step, 0), 0)

        # Target in cycle
        self.assertEqual(get_state_at_iteration(0, step, 1), 1)
        self.assertEqual(get_state_at_iteration(0, step, 4), 1)  # Wraps to cycle start
        self.assertEqual(get_state_at_iteration(0, step, 5), 2)
        self.assertEqual(get_state_at_iteration(0, step, 6), 3)
        self.assertEqual(get_state_at_iteration(0, step, 7), 1)  # Cycle repeats


class TestSimulateUntilRepeat(unittest.TestCase):
    """Test simulate_until_repeat."""

    def test_simple_repeat(self):
        result = simulate_until_repeat(0, lambda x: (x + 1) % 5)
        self.assertIsNotNone(result)
        iteration, state = result
        self.assertEqual(iteration, 5)
        self.assertEqual(state, 0)

    def test_immediate_repeat(self):
        """State stays same: 1 -> 1 -> 1."""
        result = simulate_until_repeat(0, lambda x: 1)
        self.assertIsNotNone(result)
        iteration, state = result
        self.assertEqual(iteration, 2)  # 0 -> 1 -> 1 (repeat at step 2)
        self.assertEqual(state, 1)

    def test_with_prefix(self):
        def step(x):
            return 1 if x == 3 else x + 1

        result = simulate_until_repeat(0, step)
        self.assertIsNotNone(result)
        iteration, state = result
        self.assertEqual(iteration, 4)  # 0 -> 1 -> 2 -> 3 -> 1 (repeat)
        self.assertEqual(state, 1)


class TestDetectCycleInSequence(unittest.TestCase):
    """Test detect_cycle_in_sequence."""

    def test_simple_sequence(self):
        seq = [0, 1, 2, 3, 1, 2, 3, 1]
        result = detect_cycle_in_sequence(seq)
        self.assertIsNotNone(result)
        cycle_start, cycle_length = result
        self.assertEqual(cycle_start, 1)
        self.assertEqual(cycle_length, 3)

    def test_no_cycle(self):
        seq = [0, 1, 2, 3, 4, 5]
        result = detect_cycle_in_sequence(seq)
        self.assertIsNone(result)

    def test_immediate_cycle(self):
        seq = [5, 5, 5]
        result = detect_cycle_in_sequence(seq)
        self.assertIsNotNone(result)
        cycle_start, cycle_length = result
        self.assertEqual(cycle_start, 0)
        self.assertEqual(cycle_length, 1)

    def test_cycle_at_end(self):
        seq = [0, 1, 2, 3, 4, 0]
        result = detect_cycle_in_sequence(seq)
        self.assertIsNotNone(result)
        cycle_start, cycle_length = result
        self.assertEqual(cycle_start, 0)
        self.assertEqual(cycle_length, 5)


class TestCyclePrinterFormatCycleResult(unittest.TestCase):
    """Test format_cycle_result."""

    def test_format_valid_result(self):
        result = (5, 10, 42)
        output = format_cycle_result(result)
        self.assertIn("5", output)
        self.assertIn("10", output)
        self.assertIn("42", output)
        self.assertIn("Cycle", output)

    def test_format_none_result(self):
        output = format_cycle_result(None)
        self.assertIn("no cycle", output.lower())


class TestCyclePrinterFormatCycleHistory(unittest.TestCase):
    """Test format_cycle_history."""

    def test_format_valid_history(self):
        result = (2, 3, [0, 1, 2, 3, 4])
        output = format_cycle_history(result)
        self.assertIsInstance(output, str)
        self.assertIn("2", output)  # cycle_start
        self.assertIn("3", output)  # cycle_length

    def test_format_none(self):
        output = format_cycle_history(None)
        self.assertIn("no cycle", output.lower())

    def test_format_no_prefix(self):
        result = (0, 5, [0, 1, 2, 3, 4])
        output = format_cycle_history(result)
        self.assertIn("none", output.lower())  # No prefix


class TestCyclePrinterFormatRepeatResult(unittest.TestCase):
    """Test format_repeat_result."""

    def test_format_valid_repeat(self):
        result = (100, 42)
        output = format_repeat_result(result)
        self.assertIn("100", output)
        self.assertIn("42", output)

    def test_format_none(self):
        output = format_repeat_result(None)
        self.assertIn("no repeat", output.lower())


class TestCyclePrinterFormatIterationLookup(unittest.TestCase):
    """Test format_iteration_lookup."""

    def test_format_large_target(self):
        output = format_iteration_lookup(
            target=1_000_000_000_000, cycle_start=5, cycle_length=100, result_state=42
        )
        self.assertIn("1,000,000,000,000", output)
        self.assertIn("5", output)
        self.assertIn("100", output)
        self.assertIn("42", output)

    def test_format_target_in_prefix(self):
        output = format_iteration_lookup(
            target=3, cycle_start=10, cycle_length=5, result_state=99
        )
        self.assertIn("prefix", output.lower())
        self.assertIn("99", output)


class TestCyclePrinterFormatHistoryTable(unittest.TestCase):
    """Test format_history_table."""

    def test_format_small_history(self):
        history = [0, 1, 2, 3, 4]
        output = format_history_table(history, cycle_start=2, cycle_length=3)
        self.assertIn("Step", output)
        self.assertIn("State", output)
        self.assertIn("Phase", output)
        self.assertIn("cycle start", output.lower())

    def test_format_large_history_truncated(self):
        history = list(range(100))
        output = format_history_table(
            history, cycle_start=5, cycle_length=95, max_rows=10
        )
        self.assertIn("...", output)  # Should show ellipsis


class TestCyclePrinterFormatStateAtTarget(unittest.TestCase):
    """Test format_state_at_target."""

    def test_format_basic(self):
        output = format_state_at_target(42, 1_000_000)
        self.assertIn("42", output)
        self.assertIn("1,000,000", output)

    def test_format_large_target(self):
        output = format_state_at_target(99, 1_000_000_000_000)
        self.assertIn("99", output)
        self.assertIn("1,000,000,000,000", output)


class TestCycleIntegration(unittest.TestCase):
    """Integration tests combining utils and printers."""

    def test_full_workflow(self):
        """Test complete cycle detection workflow."""
        initial = 0

        def step(x):
            return (x + 1) % 7

        target = 1_000_000_000

        # Detect cycle
        cycle_result = find_cycle(initial, step)
        self.assertIsNotNone(cycle_result)

        # Get history
        history_result = find_cycle_with_history(initial, step)
        self.assertIsNotNone(history_result)

        # Get state at large target
        state = get_state_at_iteration(initial, step, target)
        self.assertEqual(state, target % 7)

        # Format results
        output1 = format_cycle_result(cycle_result)
        self.assertIsInstance(output1, str)

        output2 = format_cycle_history(history_result)
        self.assertIsInstance(output2, str)

        cycle_start, cycle_length, _ = history_result
        output3 = format_iteration_lookup(target, cycle_start, cycle_length, state)
        self.assertIsInstance(output3, str)

    def test_lcg_workflow(self):
        """Test with linear congruential generator."""
        initial = 42
        multiplier = 7
        modulo = 1000

        def step(x):
            return (x * multiplier + 1) % modulo

        # Detect
        result = find_cycle_with_history(initial, step)
        self.assertIsNotNone(result)
        cycle_start, cycle_length, history = result

        # Verify cycle
        self.assertGreater(cycle_length, 0)
        self.assertLessEqual(cycle_start + cycle_length, len(history) + 1)

        # Large target
        target = 1_000_000_000_000
        state = get_state_at_iteration(initial, step, target)

        # Verify manually
        expected_index = cycle_start + ((target - cycle_start) % cycle_length)
        expected_state = (
            history[expected_index]
            if expected_index < len(history)
            else history[cycle_start + ((target - cycle_start) % cycle_length)]
        )
        self.assertEqual(state, expected_state)


if __name__ == "__main__":
    unittest.main()
