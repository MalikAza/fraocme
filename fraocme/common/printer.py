import statistics

from ..ui.colors import c


def print_row_stats(row: list[int]) -> None:
    """
    Print a row with colored stats:
    - Green: maximum value
    - Red: minimum value
    - Yellow: median value
    - Muted: everything else
    """
    if not row:
        print("Empty row")
        return

    min_val = min(row)
    max_val = max(row)
    median_val = statistics.median(row)
    avg_val = statistics.mean(row)
    print(
        f"📊 Stats → {c.red('Min')}: {c.red(str(min_val))} │ "
        f"{c.green('Max')}: {c.green(str(max_val))} │ "
        f"{c.yellow('Med')}: {c.yellow(str(median_val))} │ "
        f"{c.cyan('Avg')}: {c.cyan(f'{avg_val:.2f}')}"
    )

    colored = []
    for val in row:
        colored_val = c.stat(val, min_val, max_val, median_val)
        if val == avg_val:
            colored_val = c.underline(colored_val)
        colored.append(colored_val)

    print("[" + ", ".join(colored) + "]")


def print_ranges(
    ranges: list[tuple[int, int]],
    width: int = 50,
    head: int | None = 5,
    tail: int | None = None,
) -> None:
    """
    Visualize ranges on a number line with stats.

    Args:
        ranges: List of (start, end) tuples
        width: Character width for the visualization
        head: Show first N ranges (default: 5, None for all)
        tail: Show last N ranges (default: None)

    Example:
        ranges = [(1, 5), (10, 15), (20, 25)]
        print_ranges(ranges)
    """
    if not ranges:
        print("No ranges")
        return

    total = len(ranges)
    all_starts = [r[0] for r in ranges]
    all_ends = [r[1] for r in ranges]
    lengths = [end - start for start, end in ranges]

    global_min = min(all_starts)
    global_max = max(all_ends)
    span = global_max - global_min or 1

    # Stats
    min_len = min(lengths)
    max_len = max(lengths)
    avg_len = statistics.mean(lengths)
    median_len = statistics.median(lengths)
    total_coverage = sum(lengths)

    # Print summary header
    print(
        f"📏 Ranges: {c.cyan(str(total))} total │ "
        f"Span: {c.green(str(global_min))} → {c.green(str(global_max))} │ "
        f"Coverage: {c.magenta(str(total_coverage))}"
    )
    print(
        f"📊 Length → {c.red('Min')}: {c.red(str(min_len))} │ "
        f"{c.green('Max')}: {c.green(str(max_len))} │ "
        f"{c.yellow('Med')}: {c.yellow(str(median_len))} │ "
        f"{c.cyan('Avg')}: {c.cyan(f'{avg_len:.2f}')}"
    )

    # Calculate max label width for alignment
    max_label_len = max(len(f"{s}-{e}") for s, e in ranges)
    max_len_digits = len(str(max_len))

    def print_range(start: int, end: int) -> None:
        length = end - start
        label = f"{start}-{end}".rjust(max_label_len)
        length_padded = str(length).rjust(max_len_digits)
        len_str = c.stat(length, min_len, max_len, median_len)
        # Replace the number in len_str with padded version
        len_display = len_str.replace(str(length), length_padded)
        start_pos = int((start - global_min) / span * width)
        end_pos = int((end - global_min) / span * width)
        bar_len = max(1, end_pos - start_pos)
        line = (
            c.muted("·") * start_pos
            + c.green("█") * bar_len
            + c.muted("·") * (width - start_pos - bar_len)
        )
        print(f"{c.cyan(label)} ({len_display})  [{line}]")

    # Calculate ellipsis padding
    ellipsis_pad = max_label_len + max_len_digits + 6

    # Determine which ranges to show
    if head is None and tail is None:
        for start, end in ranges:
            print_range(start, end)
    else:
        head_n = head or 0
        tail_n = tail or 0

        for start, end in ranges[:head_n]:
            print_range(start, end)

        hidden = total - head_n - tail_n
        if hidden > 0:
            print(" " * ellipsis_pad + c.muted(f"... {hidden} more ..."))

        if tail_n > 0:
            for start, end in ranges[-tail_n:]:
                print_range(start, end)


def print_dict_row(data: dict[int, list[int]], key: int) -> None:
    """
    Print a single row from a dict by key with stats.

    Args:
        data: Dict from key_ints parser
        key: The key to print

    Example:
        data = {190: [10, 19], 3267: [81, 40, 27]}
        print_dict_row(data, 190)
    """
    if key not in data:
        print(f"{c.red('Key not found')}: {key}")
        return

    values = data[key]
    min_val = min(values)
    max_val = max(values)
    median_val = statistics.median(values)
    avg_val = statistics.mean(values)

    # Stats line
    print(
        f"📊 Stats → {c.red('Min')}: {c.red(str(min_val))} │ "
        f"{c.green('Max')}: {c.green(str(max_val))} │ "
        f"{c.yellow('Med')}: {c.yellow(str(median_val))} │ "
        f"{c.cyan('Avg')}: {c.cyan(f'{avg_val:.2f}')}"
    )

    # Colored values
    colored = [c.stat(val, min_val, max_val, median_val) for val in values]

    print(f"{c.cyan(str(key))} → [{', '.join(colored)}]")


def print_dict_head(data: dict[int, list[int]], n: int = 5) -> None:
    """
    Print first N rows from a dict with key stats.

    Args:
        data: Dict from key_ints parser
        n: Number of rows to print (default: 5)

    Example:
        data = {190: [10, 19], 3267: [81, 40, 27], 83: [17, 5]}
        print_dict_head(data, 2)
    """
    if not data:
        print("Empty dict")
        return

    keys = list(data.keys())
    all_keys = keys
    keys = keys[:n]

    # Key stats
    min_key = min(all_keys)
    max_key = max(all_keys)
    median_key = statistics.median(all_keys)
    avg_key = statistics.mean(all_keys)

    # Value stats (flatten all values)
    all_values = [v for vals in data.values() for v in vals]
    min_val = min(all_values)
    max_val = max(all_values)
    median_val = statistics.median(all_values)
    avg_val = statistics.mean(all_values)

    print(
        f"🔑 Keys ({c.cyan(str(len(all_keys)))}) → "
        f"{c.red('Min')}: {c.red(str(min_key))} │ "
        f"{c.green('Max')}: {c.green(str(max_key))} │ "
        f"{c.yellow('Med')}: {c.yellow(str(median_key))} │ "
        f"{c.cyan('Avg')}: {c.cyan(f'{avg_key:.2f}')}"
    )
    print(
        f"📊 Values → "
        f"{c.red('Min')}: {c.red(str(min_val))} │ "
        f"{c.green('Max')}: {c.green(str(max_val))} │ "
        f"{c.yellow('Med')}: {c.yellow(str(median_val))} │ "
        f"{c.cyan('Avg')}: {c.cyan(f'{avg_val:.2f}')}"
    )

    max_key_len = max(len(str(k)) for k in keys)

    for key in keys:
        values = data[key]
        # Color key based on all keys (+10 for ANSI codes)
        key_str = c.stat(key, min_key, max_key, median_key).rjust(max_key_len + 10)

        # Color values based on all values
        colored = [c.stat(val, min_val, max_val, median_val) for val in values]

        print(f"{key_str} → [{', '.join(colored)}]")

    remaining = len(all_keys) - n
    if remaining > 0:
        print(c.muted(f"... and {remaining} more"))
