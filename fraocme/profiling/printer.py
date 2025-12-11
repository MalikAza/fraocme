from fraocme.ui import c
from fraocme.ui.printer import print_header


def print_stats_day(day: int, data: dict, best_only: bool = False):
    if not data:
        print(c.warning(f"No stats for day {day}"))
        return

    from fraocme.ui.printer import print_section

    print_section(f"Day {day}")

    for part in ["part1", "part2"]:
        if part not in data:
            continue
        entry = data[part]
        part_name = "Part 1" if part == "part1" else "Part 2"
        if best_only:
            print(f"  {part_name}: {c.time(entry['min_ms'])}")
        else:
            print_part_stats(part_name, entry)
    print()


def print_part_stats(part_name: str, entry: dict):
    answer = entry.get("answer", "?")
    min_ms = entry.get("min_ms", 0)
    last_ms = entry.get("last_ms", 0)
    runs = entry.get("runs", 0)
    last_run = entry.get("last_run", "?")
    # Format last run date
    from datetime import datetime

    if last_run != "?":
        try:
            dt = datetime.fromisoformat(last_run)
            last_run = dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            pass
    print(f"  {c.cyan(part_name)}")
    print(f"    Answer: {c.success(str(answer))}")
    print(f"    Best:   {c.time(min_ms)}")
    print(f"    Last:   {c.time(last_ms)}")
    print(f"    Runs:   {c.muted(str(runs))}")
    print(f"    Date:   {c.muted(last_run)}")


def print_stats_summary_table(data: dict):
    if not data:
        print(c.warning("No statistics available."))
        return
    print_header("Profiling Statistics")
    # Determine column widths dynamically
    day_col = max(5, max(len(str(int(x.split("_")[1]))) for x in data.keys()))
    p1_col = 8
    p2_col = 8
    total_col = 8
    fastest_col = 8
    if any(int(x.split("_")[1]) > 999 for x in data.keys()):
        day_col = max(day_col, 6)
    print()
    # Print header with manual alignment
    sep = "  "  # Two spaces for alignment

    # Count number of days with P1 and P2 results (nonzero, not None)
    def is_valid(val):
        return val is not None and val != 0

    p1_count = sum(
        1
        for day_data in data.values()
        if is_valid(day_data.get("part1", {}).get("min_ms"))
    )
    p2_count = sum(
        1
        for day_data in data.values()
        if is_valid(day_data.get("part2", {}).get("min_ms"))
    )
    p1_header = f"P1 ({p1_count})"
    p2_header = f"P2 ({p2_count})"
    print(
        sep.join(
            [
                str("Day").rjust(day_col),
                str(p1_header).rjust(p1_col),
                str(p2_header).rjust(p2_col),
                str("Total").rjust(total_col),
                str("Fastest").rjust(fastest_col),
            ]
        )
    )
    print(
        sep.join(
            [
                "-" * day_col,
                "-" * p1_col,
                "-" * p2_col,
                "-" * total_col,
                "-" * fastest_col,
            ]
        )
    )
    days = sorted(data.keys(), key=lambda x: int(x.split("_")[1]))
    per_day = []
    total_p1 = 0.0
    total_p2 = 0.0
    count_p1 = 0
    count_p2 = 0
    fastest_candidates = []
    for day_key in days:
        day_num = int(day_key.split("_")[1])
        day_data = data[day_key]
        p1 = day_data.get("part1", {}).get("min_ms")
        p2 = day_data.get("part2", {}).get("min_ms")
        t = (p1 or 0) + (p2 or 0)
        per_day.append((day_num, p1, p2, t))
        if is_valid(p1):
            total_p1 += p1
            count_p1 += 1
        if is_valid(p2):
            total_p2 += p2
            count_p2 += 1
        # Only consider for fastest if at least one part is valid
        if is_valid(p1) or is_valid(p2):
            fastest_candidates.append((day_num, p1, p2, t))
    # Order by total time ascending for fastest, only valid days
    sorted_days = sorted(
        fastest_candidates, key=lambda x: x[3] if x[3] > 0 else float("inf")
    )
    fastest_map = {}
    for idx, (day_num, _, _, _) in enumerate(sorted_days, 1):
        fastest_map[day_num] = idx

    # Color function for fastest
    def fastest_color(rank, total):
        if rank == 1:
            return c.success(str(rank))
        elif rank == total:
            return c.error(str(rank))
        else:
            return c.warning(str(rank))

    for day_num, p1, p2, t in per_day:

        def fmt(val, width):
            if not is_valid(val):
                return "-".rjust(width)
            if val >= 1000:
                return f"{val / 1000:.2f}s".rjust(width)
            return f"{val:.2f}ms".rjust(width)

        p1_str = fmt(p1, p1_col)
        p2_str = fmt(p2, p2_col)
        t_str = fmt(t, total_col)
        # Pad before coloring
        p1_colored = color_time_str(p1 if is_valid(p1) else None, p1_str)
        p2_colored = color_time_str(p2 if is_valid(p2) else None, p2_str)
        t_colored = color_time_str(t if is_valid(t) else None, t_str)
        rank = fastest_map.get(day_num, None)
        if rank is not None:
            rank_colored = fastest_color(rank, len(fastest_candidates)).ljust(
                fastest_col
            )
        else:
            rank_colored = c.muted("-".ljust(fastest_col))
        print(
            sep.join(
                [
                    str(day_num).rjust(day_col),
                    p1_colored,
                    p2_colored,
                    t_colored,
                    rank_colored,
                ]
            )
        )
    print()
    # Separator above total line
    print("-" * (day_col + p1_col + p2_col + total_col + fastest_col + 4))
    total_ms = total_p1 + total_p2
    count_p1 + count_p2

    def fmt(val, width):
        if not val:
            return "-".rjust(width)
        if val >= 1000:
            return f"{val / 1000:.2f}s".rjust(width)
        return f"{val:.2f}ms".rjust(width)

    total_p1_str = fmt(total_p1, p1_col)
    total_p2_str = fmt(total_p2, p2_col)
    total_str = fmt(total_ms, total_col)
    print(
        sep.join(
            [
                str("Total:").rjust(day_col),
                total_p1_str,
                total_p2_str,
                total_str,
                "".rjust(fastest_col),
            ]
        )
    )
    print()


def color_time_str(ms, text):
    from fraocme.ui import c

    if ms is None:
        return c.muted(text)
    elif ms < 100:
        return c.success(text)
    elif ms < 1000:
        return c.warning(text)
    else:
        return c.error(text)
