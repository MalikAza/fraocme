import json
from datetime import datetime
from pathlib import Path
from typing import Any


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

    def reset_day(self, day: int) -> None:
        """Reset stats for a specific day."""
        day_key = f"day_{day:02d}"
        if day_key in self._data:
            del self._data[day_key]
            self.save()

    def reset_all(self) -> None:
        """Reset all stats."""
        self._data.clear()
        self.save()

    # Printing is now handled by profiling/printer.py
