from fraocme.ui import c


def print_header(text: str, width: int = 30) -> None:
    """Print a festive header with Christmas decorations."""
    border = "❄ " + "═" * (width - 4) + " ❄"
    print(f"\n{border}")
    print(f"  🎄 {text}")
    print(border)


def print_section(text: str, width: int = 30) -> None:
    """Print a section divider with winter theme."""
    stars = "⭐" * 3
    print(f"\n{stars} {text} {stars}")


def print_day_header(day: int) -> None:
    """Print a festive day header."""
    print_header("Day " + c.bold(c.green(str(day))))


def print_part_result(part: int, answer: int, elapsed_ms: float) -> None:
    """Print a successful part result with formatting."""
    part_name = "one" if part == 1 else "two"
    star = "⭐" if part == 1 else "🌟"
    formatted_answer = c.success(str(answer))
    formatted_time = c.muted(f"({c.time(elapsed_ms)})")
    print(f"  {star} Part {c.cyan(part_name)}: {formatted_answer} {formatted_time}")


def print_part_error(part: int, error: Exception) -> None:
    """Print a part error with formatting."""
    part_name = "one" if part == 1 else "two"
    print(f"  ❌ Part {c.cyan(part_name)}: {c.error(f'ERROR - {error}')}")


def print_timed(func_name: str, elapsed_ms: float) -> None:
    """Print a compact, single-line timed badge.

    Format example:
        [TIMED] parse ........ 0.01ms
    """
    label_plain = "- [TIMED]"
    time_plain = f"{elapsed_ms:.3f}ms"

    name_inner = c.cyan(func_name)
    time_inner = c.info(f"{elapsed_ms:.3f}ms")

    total_width = 48
    used = len(label_plain) + 1 + len(func_name) + 1 + len(time_plain)
    dots_count = max(1, total_width - used)
    dots_plain = "." * dots_count

    line = f"{label_plain} {name_inner} {dots_plain} {time_inner}"

    print(c.muted(line))


def print_benchmark(
    func_name: str, iterations: int, avg: float, min_t: float, max_t: float
) -> None:
    """Print benchmark stats in a compact, readable format.

    Keeps plain tokens like 'avg', 'min', 'max', and '<n> runs' so tests
    that search for those substrings continue to pass.
    """
    label = c.muted("- [") + c.muted("BENCH") + c.muted("]")

    avg_inner = c.info(f"{avg:.2f}ms")
    min_inner = c.green(f"{min_t:.2f}ms")
    max_inner = c.red(f"{max_t:.2f}ms")

    line = (
        f"{label} {c.cyan(func_name)} ({iterations} runs) "
        f"avg={avg_inner} min={min_inner} max={max_inner}"
    )

    print(c.muted(line))
