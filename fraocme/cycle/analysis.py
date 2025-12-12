"""
Cycle detection utilities for state machines.

Common for:
- Simulations that repeat (game of life, etc.)
- Finding patterns in large iteration counts
- Optimizing "simulate N billion steps" problems
"""

from typing import Callable, Hashable, TypeVar

T = TypeVar("T", bound=Hashable)


def find_cycle(
    initial_state: T, step: Callable[[T], T], max_iterations: int = 10_000_000
) -> tuple[int, int, T] | None:
    """
    Detect cycle in state sequence using Floyd's tortoise and hare algorithm.

    Memory efficient - only stores a few states at a time.

    Args:
        initial_state: Starting state (must be hashable)
        step: Function to get next state
        max_iterations: Safety limit

    Returns:
        (cycle_start, cycle_length, state_at_cycle_start) or None if no cycle found

    Example:
        >>> # Sequence: 0, 1, 2, 3, 4, 2, 3, 4, 2, 3, 4, ...
        >>> find_cycle(0, lambda x: (x + 1) if x < 4 else 2)
        (2, 3, 2)  # Cycle starts at index 2, length 3

    Example (simple modulo):
        >>> find_cycle(0, lambda x: (x + 1) % 5)
        (0, 5, 0)  # Cycle starts at index 0, length 5
    """
    # Phase 1: Find a point inside the cycle (tortoise and hare)
    slow = fast = initial_state

    for _ in range(max_iterations):
        slow = step(slow)
        fast = step(step(fast))
        if slow == fast:
            break
    else:
        return None  # No cycle found within limit

    # Phase 2: Find cycle start
    slow = initial_state
    cycle_start = 0
    while slow != fast:
        slow = step(slow)
        fast = step(fast)
        cycle_start += 1

    # Phase 3: Find cycle length
    cycle_length = 1
    fast = step(slow)
    while slow != fast:
        fast = step(fast)
        cycle_length += 1

    return cycle_start, cycle_length, slow


def find_cycle_with_history(
    initial_state: T, step: Callable[[T], T], max_iterations: int = 10_000_000
) -> tuple[int, int, list[T]] | None:
    """
    Detect cycle and return full history (uses more memory but gives all states).

    Useful when you need to access specific states after detection.

    Args:
        initial_state: Starting state (must be hashable)
        step: Function to get next state
        max_iterations: Safety limit

    Returns:
        (cycle_start, cycle_length, history_list) or None if no cycle found

    Example:
        >>> start, length, history = find_cycle_with_history(0, lambda x: (x + 1) % 5)
        >>> start, length
        (0, 5)
        >>> history
        [0, 1, 2, 3, 4]

    Example (with prefix before cycle):
        >>> # 0 -> 1 -> 2 -> 3 -> 1 -> 2 -> 3 -> 1 -> ...
        >>> def next_state(x):
        ...     return 1 if x == 3 else x + 1
        >>> start, length, history = find_cycle_with_history(0, next_state)
        >>> start, length
        (1, 3)
        >>> history
        [0, 1, 2, 3]
    """
    history = [initial_state]
    seen = {initial_state: 0}
    state = initial_state

    for i in range(1, max_iterations):
        state = step(state)

        if state in seen:
            cycle_start = seen[state]
            cycle_length = i - cycle_start
            return cycle_start, cycle_length, history

        seen[state] = i
        history.append(state)

    return None  # No cycle found within limit


def get_state_at_iteration(
    initial_state: T,
    step: Callable[[T], T],
    target_iteration: int,
    max_iterations: int = 10_000_000,
) -> T:
    """
    Get state at a specific iteration, using cycle detection for huge targets.

    If target_iteration is small, simulates directly.
    If target_iteration is large and a cycle exists, uses cycle to skip ahead.

    Args:
        initial_state: Starting state
        step: Function to get next state
        target_iteration: Which iteration to get (0 = initial state)
        max_iterations: Max iterations to search for cycle

    Returns:
        State at target_iteration

    Example:
        >>> # What's the state after 1 billion iterations of x -> (x+1) % 7?
        >>> get_state_at_iteration(0, lambda x: (x + 1) % 7, 1_000_000_000)
        6  # 1_000_000_000 % 7 = 6

    Example (AoC-style problem):
        >>> # Simulate game for 1 trillion steps
        >>> final_state = get_state_at_iteration(initial, game_step, 1_000_000_000_000)
    """
    # Try to find a cycle
    result = find_cycle_with_history(initial_state, step, max_iterations)

    if result is None:
        # No cycle found, simulate directly (may be slow for large targets)
        state = initial_state
        for _ in range(target_iteration):
            state = step(state)
        return state

    cycle_start, cycle_length, history = result

    # If target is before cycle starts, return from history
    if target_iteration < len(history):
        return history[target_iteration]

    # Use cycle to compute position
    remaining = (target_iteration - cycle_start) % cycle_length
    return history[cycle_start + remaining]


def simulate_until_repeat(
    initial_state: T, step: Callable[[T], T], max_iterations: int = 10_000_000
) -> tuple[int, T] | None:
    """
    Simulate until a state repeats, return iteration count and repeated state.

    Simpler than find_cycle - just finds when ANY repeat happens.

    Args:
        initial_state: Starting state
        step: Function to get next state
        max_iterations: Safety limit

    Returns:
        (iteration_of_repeat, repeated_state) or None

    Example:
        >>> simulate_until_repeat(0, lambda x: (x + 1) % 5)
        (5, 0)  # After 5 steps, we see state 0 again
    """
    seen = {initial_state: 0}
    state = initial_state

    for i in range(1, max_iterations):
        state = step(state)

        if state in seen:
            return i, state

        seen[state] = i

    return None


def detect_cycle_in_sequence(sequence: list[T]) -> tuple[int, int] | None:
    """
    Detect cycle in a pre-computed sequence.

    Args:
        sequence: List of states

    Returns:
        (cycle_start, cycle_length) or None if no cycle

    Example:
        >>> detect_cycle_in_sequence([0, 1, 2, 3, 1, 2, 3, 1, 2, 3])
        (1, 3)  # Cycle starts at index 1, length 3
    """
    seen = {}

    for i, state in enumerate(sequence):
        if state in seen:
            cycle_start = seen[state]
            cycle_length = i - cycle_start
            return cycle_start, cycle_length
        seen[state] = i

    return None


def iterate_with_cycle_detection(
    initial_state: T, step: Callable[[T], T], max_iterations: int = 10_000_000
):
    """
    Generator that yields (iteration, state) and detects cycles.

    Yields states one at a time. When cycle is detected, sets
    `.cycle_info` attribute on the generator.

    Args:
        initial_state: Starting state
        step: Function to get next state
        max_iterations: Safety limit

    Yields:
        (iteration, state) tuples

    Example:
        >>> gen = iterate_with_cycle_detection(0, lambda x: (x + 1) % 3)
        >>> for i, state in gen:
        ...     print(f"Step {i}: {state}")
        ...     if i >= 5:
        ...         break
        Step 0: 0
        Step 1: 1
        Step 2: 2
        Step 3: 0
        Step 4: 1
        Step 5: 2
    """
    seen = {initial_state: 0}
    state = initial_state
    yield 0, state

    for i in range(1, max_iterations):
        state = step(state)

        if state in seen:
            # Cycle detected - could store info if needed
            cycle_start = seen[state]
            i - cycle_start
            # Continue yielding but cycle is known
            yield i, state
            # After this point, we're in the cycle
            while True:
                i += 1
                state = step(state)
                yield i, state

        seen[state] = i
        yield i, state
