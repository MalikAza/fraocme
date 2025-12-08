import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fraocme.ui import c


class Stats:
    """Track and display solution statistics."""

    def __init__(self, path: Path | None = None):
        self.path = path or Path.cwd() / "stats.json"
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict:
        """Load stats from file."""
        if self.path.exists():
            try:
                return json.loads(self.path.read_text())
            except json.JSONDecodeError:
                return {}
        return {}

    def save(self) -> None:
        """Save stats to file."""
        self.path.write_text(json.dumps(self._data, indent=2))

    def update(self, day: int, results: dict[int, tuple[int, float]]) -> None:
        """
        Update stats for a day.

        Args:
            day: Day number
            results: Dict of {part: (answer, time_ms)}
        """
        day_key = f"day_{day:02d}"

        if day_key not in self._data:
            self._data[day_key] = {}

        now = datetime.now().isoformat()

        for part, (answer, time_ms) in results.items():
            part_key = f"part{part}"

            if part_key not in self._data[day_key]:
                self._data[day_key][part_key] = {
                    "answer": answer,
                    "min_ms": time_ms,
                    "last_ms": time_ms,
                    "last_run": now,
                    "runs": 1,
                }
            else:
                entry = self._data[day_key][part_key]
                entry["answer"] = answer
                entry["last_ms"] = time_ms
                entry["last_run"] = now
                entry["runs"] = entry.get("runs", 0) + 1

                # Update min if beaten
                if time_ms < entry["min_ms"]:
                    entry["min_ms"] = time_ms

    def get_day(self, day: int) -> dict | None:
        """Get stats for a specific day."""
        return self._data.get(f"day_{day:02d}")

    def get_all(self) -> dict:
        """Get all stats."""
        return self._data.copy()

    # ─────────────────────────────────────────────────────────
    # Printing
    # ─────────────────────────────────────────────────────────

    def print_day(self, day: int, best_only: bool = False) -> None:
        """Print stats for a specific day."""
        data = self.get_day(day)

        if not data:
            print(c.warning(f"No stats for day {day}"))
            return

        print(f"\n{c.bold(c.cyan(f'Day {day}'))}")
        print("─" * 40)

        for part in ["part1", "part2"]:
            if part not in data:
                continue

            entry = data[part]
            part_name = "Part 1" if part == "part1" else "Part 2"

            if best_only:
                print(f"  {part_name}: {c.time(entry['min_ms'])}")
            else:
                self._print_part_stats(part_name, entry)

        print()

    def print_all(self, best_only: bool = False) -> None:
        """Print stats for all days."""
        if not self._data:
            print(c.warning("No stats recorded yet"))
            return

        print(f"\n{c.bold('═' * 50)}")
        print(c.bold("  Advent of Code Stats"))
        print(c.bold("═" * 50))

        if best_only:
            self._print_summary_table()
        else:
            # Sort by day number
            days = sorted(self._data.keys(), key=lambda x: int(x.split("_")[1]))
            for day_key in days:
                day_num = int(day_key.split("_")[1])
                self.print_day(day_num, best_only=False)

        self._print_totals()

    def _print_part_stats(self, part_name: str, entry: dict) -> None:
        """Print detailed stats for a part."""
        answer = entry.get("answer", "?")
        min_ms = entry.get("min_ms", 0)
        last_ms = entry.get("last_ms", 0)
        runs = entry.get("runs", 0)
        last_run = entry.get("last_run", "?")

        # Format last run date
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

    def _print_summary_table(self) -> None:
        """Print compact summary table."""
        print(f"\n  {'Day':<6} {'Part 1':<14} {'Part 2':<14}")
        print(f"  {'-' * 6} {'-' * 14} {'-' * 14}")

        days = sorted(self._data.keys(), key=lambda x: int(x.split("_")[1]))

        for day_key in days:
            day_num = int(day_key.split("_")[1])
            data = self._data[day_key]

            p1 = data.get("part1", {}).get("min_ms")
            p2 = data.get("part2", {}).get("min_ms")

            p1_str = f"{p1:.2f}ms" if p1 else "-"
            p2_str = f"{p2:.2f}ms" if p2 else "-"

            p1_colored = self._color_time_str(p1, p1_str)
            p2_colored = self._color_time_str(p2, p2_str)

            print(f"  {day_num:<6} {p1_colored:<23} {p2_colored:<23}")

        print()

    def _color_time_str(self, ms: float | None, text: str) -> str:
        """Color a time string based on value."""
        if ms is None:
            return c.muted(text)
        elif ms < 100:
            return c.success(text)
        elif ms < 1000:
            return c.warning(text)
        else:
            return c.error(text)

    def _print_totals(self) -> None:
        """Print total time across all solutions."""
        total_ms = 0.0
        total_parts = 0

        for day_data in self._data.values():
            for part in ["part1", "part2"]:
                if part in day_data:
                    total_ms += day_data[part].get("min_ms", 0)
                    total_parts += 1

        print("─" * 50)

        if total_ms < 1000:
            total_str = f"{total_ms:.2f}ms"
        else:
            total_str = f"{total_ms / 1000:.2f}s"

        print(f"  Total ({total_parts} parts): {c.bold(total_str)}")
        print()
