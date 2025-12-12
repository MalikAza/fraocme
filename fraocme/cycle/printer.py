"""
Formatters for cycle detection results.

These are pure formatters - no logic, just display pre-computed data.
"""

from typing import Sequence, TypeVar

from fraocme.ui.colors import c

T = TypeVar("T")


def format_cycle_result(
    result: tuple[int, int, T] | None,
) -> str:
    """
    Format result from find_cycle().

    Args:
        result: (cycle_start, cycle_length, state_at_start) or None

    Example:
        >>> result = find_cycle(initial, step)
        >>> print(format_cycle_result(result))
    """
    if result is None:
        return c.red("No cycle found")

    cycle_start, cycle_length, state_at_start = result

    lines = []
    lines.append(c.bold("Cycle detected:"))
    lines.append(f"  Start index: {c.yellow(cycle_start)}")
    lines.append(f"  Cycle length: {c.magenta(cycle_length)}")
    lines.append(f"  State at start: {c.cyan(state_at_start)}")

    return "\n".join(lines)


def format_cycle_history(
    result: tuple[int, int, list[T]] | None,
    max_prefix: int = 5,
    max_cycle: int = 10,
) -> str:
    """
    Format result from find_cycle_with_history().

    Args:
        result: (cycle_start, cycle_length, history) or None
        max_prefix: Max prefix states to show
        max_cycle: Max cycle states to show

    Example:
        >>> result = find_cycle_with_history(initial, step)
        >>> print(format_cycle_history(result))
    """
    if result is None:
        return c.red("No cycle found")

    cycle_start, cycle_length, history = result

    lines = []
    lines.append(c.bold("Cycle with history:"))
    lines.append(f"  Start index: {c.yellow(cycle_start)}")
    lines.append(f"  Cycle length: {c.magenta(cycle_length)}")
    lines.append(f"  Total states: {c.cyan(len(history))}")
    lines.append("")

    # Prefix
    if cycle_start > 0:
        prefix = history[: min(cycle_start, max_prefix)]
        prefix_str = c.dim(" → ").join(c.yellow(str(s)) for s in prefix)
        if cycle_start > max_prefix:
            prefix_str += c.dim(f" → ... ({cycle_start - max_prefix} more)")
        lines.append(f"  {c.dim('Prefix:')} {prefix_str}")
    else:
        lines.append(f"  {c.dim('Prefix:')} {c.dim('(none)')}")

    # Cycle
    cycle_end = min(cycle_start + cycle_length, len(history))
    cycle_states = history[cycle_start:cycle_end]

    if len(cycle_states) <= max_cycle:
        cycle_str = c.green(" → ").join(c.cyan(str(s)) for s in cycle_states)
    else:
        cycle_str = c.green(" → ").join(
            c.cyan(str(s)) for s in cycle_states[:max_cycle]
        )
        cycle_str += c.dim(f" → ... ({len(cycle_states) - max_cycle} more)")

    lines.append(f"  {c.dim('Cycle:')}  [{cycle_str}] {c.green('↺')}")

    return "\n".join(lines)


def format_repeat_result(
    result: tuple[int, T] | None,
) -> str:
    """
    Format result from simulate_until_repeat().

    Args:
        result: (iteration, repeated_state) or None

    Example:
        >>> result = simulate_until_repeat(initial, step)
        >>> print(format_repeat_result(result))
    """
    if result is None:
        return c.red("No repeat found")

    iteration, state = result

    return f"First repeat at iteration {c.green(iteration)}, state: {c.cyan(state)}"


def format_iteration_lookup(
    target: int,
    cycle_start: int,
    cycle_length: int,
    result_state: T,
) -> str:
    """
    Format the calculation for get_state_at_iteration().

    Args:
        target: Target iteration
        cycle_start: Where cycle starts
        cycle_length: Length of cycle
        result_state: The computed state

    Example:
        >>> result = find_cycle_with_history(initial, step)
        >>> cycle_start, cycle_length, history = result
        >>> state = get_state_at_iteration(initial, step, target)
        >>> print(format_iteration_lookup(target, cycle_start, cycle_length, state))
    """
    lines = []
    lines.append(c.bold("Iteration lookup:"))
    lines.append(f"  Target: {c.cyan(f'{target:,}')}")
    lines.append(f"  Cycle start: {c.yellow(cycle_start)}")
    lines.append(f"  Cycle length: {c.magenta(cycle_length)}")
    lines.append(c.dim("  " + "─" * 30))

    if target < cycle_start:
        lines.append(f"  Target in prefix: history[{c.cyan(target)}]")
    else:
        remaining = target - cycle_start
        position = remaining % cycle_length
        index = cycle_start + position

        lines.append(f"  Steps after start: {c.yellow(f'{remaining:,}')}")
        lines.append(
            f"  Position: {c.yellow(f'{remaining:,}')} mod {c.magenta(cycle_length)} = {
                c.green(position)
            }"
        )
        lines.append(
            f"  Index: {c.yellow(cycle_start)} + {c.green(position)} = {c.cyan(index)}"
        )

    lines.append(c.dim("  " + "─" * 30))
    lines.append(f"  Result: {c.bold(c.green(result_state))}")

    return "\n".join(lines)


def format_history_table(
    history: Sequence[T],
    cycle_start: int,
    cycle_length: int,
    max_rows: int = 20,
) -> str:
    """
    Format history as a table.

    Args:
        history: State history list
        cycle_start: Where cycle starts
        cycle_length: Length of cycle
        max_rows: Max rows to display

    Example:
        >>> result = find_cycle_with_history(initial, step)
        >>> cycle_start, cycle_length, history = result
        >>> print(format_history_table(history, cycle_start, cycle_length))
    """
    lines = []
    lines.append(c.bold(f"{'Step':>5} │ {'State':>10} │ Phase"))
    lines.append(c.dim("─" * 5 + "┼" + "─" * 12 + "┼" + "─" * 15))

    # Determine which rows to show
    total = len(history)
    if total <= max_rows:
        indices = list(range(total))
        ellipsis_idx = -1
    else:
        first = max_rows * 2 // 3
        last = max_rows - first - 1
        indices = list(range(first)) + list(range(total - last, total))
        ellipsis_idx = first

    for i, idx in enumerate(indices):
        state = history[idx]

        # Phase label
        if idx < cycle_start:
            phase = c.yellow("prefix")
            state_str = c.yellow(str(state))
        elif idx == cycle_start:
            phase = c.green("← cycle start")
            state_str = c.cyan(str(state))
        else:
            pos = idx - cycle_start
            phase = c.cyan(f"cycle[{pos}]")
            state_str = c.cyan(str(state))

        lines.append(f"{idx:>5} │ {state_str:>10} │ {phase}")

        if i == ellipsis_idx - 1 and ellipsis_idx > 0:
            hidden = total - max_rows
            lines.append(c.dim(f"  ... │ {'...':>10} │ ({hidden} more)"))

    return "\n".join(lines)


def format_state_at_target(
    state: T,
    target: int,
) -> str:
    """
    Format result from get_state_at_iteration().

    Example:
        >>> state = get_state_at_iteration(initial, step, 1_000_000_000)
        >>> print(format_state_at_target(state, 1_000_000_000))
    """
    return f"State at iteration {c.cyan(f'{target:,}')}: {c.bold(c.green(state))}"
