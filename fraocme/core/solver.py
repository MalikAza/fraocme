from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar
from copy import deepcopy
import time
import traceback
from fraocme.ui import c
from fraocme.ui.printer import print_header

T = TypeVar('T')


class Solver(ABC):
    """
    Base class for Advent of Code solutions.
    
    Subclass this and implement:
        - parse(raw) -> Any
        - part1(data) -> int
        - part2(data) -> int
    """
    
    def __init__(self, day: int | None = None, debug: bool = False, copy_input: bool = True):
        self.day = day
        self.debug_enabled = debug
        self.copy_input = copy_input
        self._input_dir: Path | None = None
    
    # ─────────────────────────────────────────────────────────
    # Abstract methods 
    # ─────────────────────────────────────────────────────────
    
    @abstractmethod
    def parse(self, raw: str) -> T:
        """Parse raw input string into your data structure."""
        ...
    
    @abstractmethod
    def part1(self, data: T) -> int:
        """Solve part 1."""
        ...
    
    @abstractmethod
    def part2(self, data: T) -> int:
        """Solve part 2."""
        ...
    
    # ─────────────────────────────────────────────────────────
    # Input handling
    # ─────────────────────────────────────────────────────────
    
    def set_input_dir(self, path: Path) -> 'Solver':
        """Set the directory containing input.txt."""
        self._input_dir = path
        return self
    
    def load(self) -> T:
        """Load and parse input."""
        if self._input_dir is None:
            raise ValueError("Input directory not set")
        
        path = self._input_dir / "input.txt"
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
        print_header("Day " + c.bold(c.green(self.day)))
        results: dict[int, tuple[int | None, float]] = {}

        for part in parts:
            results[part] = self._run_part(part)

        print()

        return results
    
    def _run_part(self, part: int) -> tuple[int | None, float]:
        part_name = "one" if part == 1 else "two"
        
        try:
            data = self.load()
            func = self.part1 if part == 1 else self.part2
            
            start = time.perf_counter()
            answer = func(data)
            elapsed_ms = (time.perf_counter() - start) * 1000
            
            print(f"  Part {c.cyan(part_name)}: {c.success(str(answer))} {c.time(elapsed_ms)}")
            
            return answer, elapsed_ms
            
        except Exception as e:
            print(f"  Part {c.cyan(part_name)}: {c.error(f'ERROR - {e}')}")
            if self.debug_enabled:
                # TODO: add a traceback flag rather than using debug?
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