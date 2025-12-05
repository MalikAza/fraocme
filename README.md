# Fraocme

A compact, testable framework for writing Advent of Code solutions in Python.

**Goals:** simple project layout, helpful debug utilities, and reproducible timing/stats.

**Install (editable)**

```bash
pip install -e .
```

**Tests**

```bash
python -m unittest discover -v tests/
```
or
```bash
uv run test
```

**Quick Start**

1. Create a day folder with template files:
   ```bash
   fraocme create 1
   ```
2. Edit the generated `days/day_01/solution.py` and implement `part1` and `part2` methods.
3. Add your puzzle input to `days/day_01/input.txt`.
4. Run it with the CLI: `fraocme run 1`.

Example `Day0` (compact):

```python
from fraocme import Solver
from fraocme.debug.printer import print_max_in_rows
from fraocme.parsers import int_grid

class Day0(Solver):
    def __init__(self, debug: bool = False):
        super().__init__(day=0, debug=debug, copy_input=True)

    def parse(self, raw: str) -> list[list[int]]:
        # Example parser: convert input to a grid of integers
        return int_grid(raw)

    def part1(self, data: list[list[int]]) -> int:
        # Example: only run the pretty-print helper when --debug is used
        self.debug(lambda: print_max_in_rows(data))
        return sum(max(line) for line in data)

    def part2(self, data: list[list[int]]) -> int:
        return sum(sum(line) for line in data)
```

Notes:
- Use `--debug` to enable debug prints; passing callables like `lambda: ...` avoids
  evaluating expensive debug helpers when debug is disabled.
- `copy_input=True` makes `load()` return a deep copy so multiple parts won't mutate
  the same data instance.

**CLI Overview**

- **Create** a new day solution:
  ```bash
  fraocme create <day>  # Creates days/day_XX/ with solution.py and input.txt
                        # Day must be between 1 and 25
  ```
- **Run** solutions:
  ```bash
  fraocme run <day>          # Run a specific day
  fraocme run 1 -p 1         # Run only part 1
  fraocme run 1 --debug      # Run with debug output
  fraocme run --all          # Run all days
  ```
- **View** statistics:
  ```bash
  fraocme stats              # Show all stats
  fraocme stats 1            # Show stats for day 1
  fraocme stats --best       # Show only best times
  ```

**Parsers & Utilities**

Import useful parsers from `fraocme.parsers` (examples):

```python
from fraocme.parsers import int_grid, lines, ints, blocks
```

There is also a `Grid` class and helpers for points/directions used in grid-style puzzles.

**Debugging**

Call `self.debug(...)` inside your `Solver` methods. If you need to avoid evaluating
expressions unless debug is enabled, pass a callable:

```python
self.debug(lambda: expensive_debug_print(data))
```

**Stats & Timing**

Run times are collected by the framework and can be saved to `stats.json`. Some helper
decorators (e.g. `@timed`, `@benchmark`) are available under `fraocme.profiling`.

**Code Quality**

The project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```bash
# Check for linting issues
uv run ruff check .

# Format code
uv run ruff format .

# Fix fixable issues
uv run ruff check --fix .
```

**Tests**

See [tests/README.md](tests/README.md) for test organization and running tests.

---

# TODO: all the tests...
# TODO: check __init__.py for missing imports (or extra ones)