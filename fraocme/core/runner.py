import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Type

from .solver import Solver


class Runner:
    """Discovers and runs solver solutions."""

    def __init__(self, base_dir: Path | None = None):
        # Default to ./days in current working directory
        self.base_dir = base_dir or Path.cwd() / "days"

    def get_day_dir(self, day: int) -> Path:
        """Get directory for a specific day."""
        return self.base_dir / f"day_{day:02d}"

    def day_exists(self, day: int) -> bool:
        """Check if a day solution exists."""
        day_dir = self.get_day_dir(day)
        return (day_dir / "solution.py").exists()

    def get_all_days(self) -> list[int]:
        """Get list of all available days."""
        days = []
        if not self.base_dir.exists():
            return days

        for day_dir in self.base_dir.iterdir():
            if day_dir.is_dir() and day_dir.name.startswith("day_"):
                try:
                    day_num = int(day_dir.name.split("_")[1])
                    if (day_dir / "solution.py").exists():
                        days.append(day_num)
                except ValueError:
                    continue

        return sorted(days)

    def load_solver(
        self, day: int, debug: bool = False, show_traceback: bool = True
    ) -> Solver:
        """Import and instantiate a solver for a given day."""
        day_dir = self.get_day_dir(day)
        solution_file = day_dir / "solution.py"

        if not solution_file.exists():
            raise FileNotFoundError(f"No solution found for day {day}")

        # Load module from file path
        spec = importlib.util.spec_from_file_location(
            f"day_{day:02d}_solution", solution_file
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load solution for day {day}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        # Find the Solver subclass
        solver_class = self._find_solver_class(module)
        if solver_class is None:
            raise ValueError(f"No Solver subclass found in day {day}")

        # Instantiate and configure
        solver = solver_class(day=day, debug=debug, show_traceback=show_traceback)
        solver.set_input_dir(day_dir)

        return solver

    def _find_solver_class(self, module) -> Type[Solver] | None:
        """Find the Solver subclass in a module."""
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, Solver) and obj is not Solver:
                return obj
        return None

    def run_day(
        self,
        day: int,
        parts: list[int] = [1, 2],
        debug: bool = False,
        show_traceback: bool = True,
    ) -> dict[int, tuple[int, float]]:
        """Run a specific day."""
        solver = self.load_solver(day, debug=debug, show_traceback=show_traceback)
        return solver.run(parts)

    def run_all(
        self,
        parts: list[int] = [1, 2],
        debug: bool = False,
        show_traceback: bool = True,
    ) -> dict[int, dict[int, tuple[int, float]]]:
        """Run all available days."""
        results = {}
        for day in self.get_all_days():
            try:
                results[day] = self.run_day(day, parts, debug, show_traceback)
            except Exception as e:
                print(f"\033[91mDay {day} failed: {e}\033[0m")
        return results
