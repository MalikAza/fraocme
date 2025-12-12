"""
Cycle detection utilities for state machines.

Common for:
- Simulations that repeat (game of life, etc.)
- Finding patterns in large iteration counts
- Optimizing "simulate N billion steps" problems

Usage:
    from fraocme.cycle import find_cycle, get_state_at_iteration
    from fraocme.cycle.printer import format_cycle_result, format_iteration_lookup
"""

from .analysis import (
    detect_cycle_in_sequence,
    find_cycle,
    find_cycle_with_history,
    get_state_at_iteration,
    simulate_until_repeat,
)
from .printer import (
    format_cycle_history,
    format_cycle_result,
    format_history_table,
    format_iteration_lookup,
    format_repeat_result,
    format_state_at_target,
)

__all__ = [
    # analysis
    "find_cycle",
    "find_cycle_with_history",
    "get_state_at_iteration",
    "simulate_until_repeat",
    "detect_cycle_in_sequence",
    # Printers
    "format_cycle_result",
    "format_cycle_history",
    "format_repeat_result",
    "format_iteration_lookup",
    "format_history_table",
    "format_state_at_target",
]
