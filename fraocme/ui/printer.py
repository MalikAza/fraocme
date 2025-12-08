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
    formatted_time = c.muted("(") + c.muted(c.time(elapsed_ms)) + c.muted(")")
    print(f"  {star} Part {c.cyan(part_name)}: {formatted_answer} {formatted_time}")


def print_part_error(part: int, error: Exception) -> None:
    """Print a part error with formatting."""
    part_name = "one" if part == 1 else "two"
    print(f"  ❌ Part {c.cyan(part_name)}: {c.error(f'ERROR - {error}')}")
