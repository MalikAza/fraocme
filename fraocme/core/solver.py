import time
import traceback
from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from typing import TypeVar

from fraocme.ui import c
from fraocme.ui.printer import (
    print_day_header,
    print_part_error,
    print_part_result,
)

T = TypeVar("T")


class Solver(ABC):
    """
    Base class for Advent of Code solutions.

    Subclass this and implement:
        - parse(raw) -> Any
        - part1(data) -> int
        - part2(data) -> int
    """

    def __init__(
        self,
        day: int | None = None,
        copy_input: bool = True,
        debug: bool = False,
        show_traceback: bool = True,
        use_example: bool = False,
    ):
        self.day = day
        self.copy_input = copy_input
        self.debug_enabled = debug
        self.show_traceback = show_traceback
        self.use_example = use_example
        self._input_dir: Path | None = None

    # ─────────────────────────────────────────────────────────
    # Abstract methods
    # ─────────────────────────────────────────────────────────

    @abstractmethod
    def parse(self, raw: str) -> T:
        """Parse raw input string into your data structure."""
        raise NotImplementedError("This method must be implemented to be used.")

    @abstractmethod
    def part1(self, data: T) -> int:
        """Solve part 1."""
        raise NotImplementedError("This method must be implemented to be used.")

    @abstractmethod
    def part2(self, data: T) -> int:
        """Solve part 2."""
        raise NotImplementedError("This method must be implemented to be used.")

    # ─────────────────────────────────────────────────────────
    # Input handling
    # ─────────────────────────────────────────────────────────

    def set_input_dir(self, path: Path) -> "Solver":
        """Set the directory containing input.txt."""
        self._input_dir = path
        return self

    def load(self) -> T:
        """Load and parse input."""
        if self._input_dir is None:
            raise ValueError("Input directory not set")

        filename = "example_input.txt" if self.use_example else "input.txt"
        path = self._input_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Input not found: {path}")

        raw = path.read_text().strip()
        parsed = self.parse(raw)

        return deepcopy(parsed) if self.copy_input else parsed

    # ─────────────────────────────────────────────────────────
    # Execution
    # ─────────────────────────────────────────────────────────

    def run(self, parts: list[int] = [1, 2]) -> None:
        """Run and print results."""
        print_day_header(self.day)
        results: dict[int, tuple[int | None, float]] = {}

        for part in parts:
            results[part] = self._run_part(part)

        print()

        return results

    def _run_part(self, part: int) -> tuple[int | None, float]:
        try:
            data = self.load()
            func = self.part1 if part == 1 else self.part2

            start = time.perf_counter()
            answer = func(data)
            elapsed_ms = (time.perf_counter() - start) * 1000

            print_part_result(part, answer, elapsed_ms)

            return answer, elapsed_ms

        except Exception as e:
            print_part_error(part, e)
            if self.show_traceback:
                tb = traceback.format_exc()
                print(c.muted(tb))
            return None, 0.0

    # ─────────────────────────────────────────────────────────
    # Debug helper
    # ─────────────────────────────────────────────────────────

    def debug(self, *args, **kwargs) -> None:
        """Print only if debug mode is enabled."""
        if not self.debug_enabled:
            return

        processed_args = []
        for a in args:
            if callable(a):
                try:
                    res = a()
                    if res is not None:
                        processed_args.append(res)
                except Exception as e:
                    processed_args.append(f"<debug callable raised: {e}>")
            else:
                processed_args.append(a)

        print(*processed_args, **kwargs)
