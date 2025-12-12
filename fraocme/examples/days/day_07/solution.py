"""
Day 07: Cycle Detection Example

Demonstrates cycle detection utilities and formatters.
"""

from fraocme import Solver
from fraocme.cycle.analysis import (
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
from fraocme.graph.parser import parse_adjacency_list
from fraocme.ui.colors import c


class Day7(Solver):
    def parse(self, raw: str) -> dict[str, int]:
        """
        Parse configuration.

        Expected format:
            initial: 42
            multiplier: 7
            modulo: 1000
        """
        parsed = parse_adjacency_list(raw, separator=": ", key_type=str, value_type=int)

        config = {k: v[0] if v else 0 for k, v in parsed.items()}

        self.debug(f"  Initial: {c.cyan(config['initial'])}")
        self.debug(f"  Multiplier: {c.yellow(config['multiplier'])}")
        self.debug(f"  Modulo: {c.magenta(config['modulo'])}")

        return config

    def _step(self, config: dict[str, int]):
        """Create step function."""
        m, mod = config["multiplier"], config["modulo"]
        return lambda s: (s * m + 1) % mod

    def part1(self, config: dict[str, int]) -> int:
        """
        Part 1: Find when the state first repeats.
        """
        initial = config["initial"]
        step = self._step(config)

        self.debug(c.bold("\n" + "═" * 50))
        self.debug(c.bold("  Part 1: Find First Repeat"))
        self.debug(c.bold("═" * 50))

        # 1. Simple repeat detection
        repeat_result = simulate_until_repeat(initial, step)
        self.debug("")
        self.debug(format_repeat_result(repeat_result))

        if repeat_result is None:
            return -1

        repeat_iteration, _ = repeat_result

        # 2. Full cycle analysis
        cycle_result = find_cycle(initial, step)
        self.debug("")
        self.debug(format_cycle_result(cycle_result))

        # 3. Cycle with history
        history_result = find_cycle_with_history(initial, step)
        self.debug("")
        self.debug(format_cycle_history(history_result))

        # 4. History table
        if history_result:
            cycle_start, cycle_length, history = history_result
            self.debug("")
            self.debug(
                format_history_table(history, cycle_start, cycle_length, max_rows=15)
            )

        return repeat_iteration

    def part2(self, config: dict[str, int]) -> int:
        """
        Part 2: State after 1 trillion steps.
        """
        initial = config["initial"]
        step = self._step(config)
        target = 1_000_000_000_000

        self.debug(c.bold("\n" + "═" * 50))
        self.debug(c.bold("  Part 2: State After 1 Trillion Steps"))
        self.debug(c.bold("═" * 50))

        # 1. Detect cycle
        history_result = find_cycle_with_history(initial, step)
        self.debug("")
        self.debug(format_cycle_history(history_result))

        if history_result is None:
            self.debug(c.red("Cannot compute without cycle!"))
            return -1

        cycle_start, cycle_length, history = history_result

        # 2. Get state at target
        state = get_state_at_iteration(initial, step, target)

        # 3. Show calculation
        self.debug("")
        self.debug(format_iteration_lookup(target, cycle_start, cycle_length, state))

        # 4. Final result
        self.debug("")
        self.debug(format_state_at_target(state, target))

        return state
