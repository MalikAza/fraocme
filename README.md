# 🎄 Fraocme

[![Tests](https://github.com/MalikAza/fraocme/actions/workflows/test.yml/badge.svg)](https://github.com/MalikAza/fraocme/actions/workflows/test.yml)
[![Lint](https://github.com/MalikAza/fraocme/actions/workflows/lint.yml/badge.svg)](https://github.com/MalikAza/fraocme/actions/workflows/lint.yml)
[![Format](https://github.com/MalikAza/fraocme/actions/workflows/format.yml/badge.svg)](https://github.com/MalikAza/fraocme/actions/workflows/format.yml)
[![codecov](https://codecov.io/gh/MalikAza/fraocme/branch/main/graph/badge.svg)](https://codecov.io/gh/MalikAza/fraocme)

> *Your cozy companion for solving Advent of Code puzzles in Python* ☕✨

Fraocme is a lightweight framework that makes tackling those December coding challenges a breeze. Think clean project structure, helpful debugging tools, and automated timing—all wrapped up like a present under the tree.

**What's Inside:**
- 🎁 Simple project scaffolding
- 🐛 Smart debug utilities
- ⏱️ Performance tracking & stats
- 🎨 Pretty output formatting

## 🎅 Installation

```bash
pip install -e .
```

## 🚀 Quick Start

Get unwrapping your first puzzle in seconds:

1. **Create** a new day solution:
   ```bash
   fraocme create 1
   ```
   
2. **Edit** `days/day_01/solution.py` and implement your `parse`, `part1`, and `part2` methods.

3. **Add** your puzzle input to `days/day_01/input.txt`.

4. **Run** it:
   ```bash
   fraocme run 1
   ```

That's it! 🎉

## 📝 Example Solution

Here's what a typical solution looks like:

```python
from fraocme import Solver
from fraocme.common.parser import char_lines

class Day1(Solver):
    def parse(self, raw: str) -> list[list[int]]:
        # Parse each line into individual digits
        return char_lines(raw)

    def part1(self, data: list[list[int]]) -> int:
        # Use debug helpers during development
        self.debug("Processing", len(data), "lines")
        return sum(max(line) for line in data)

    def part2(self, data: list[list[int]]) -> int:
        return sum(sum(line) for line in data)
```

**Pro Tips:**
- 🐛 Pass callables to `self.debug(lambda: expensive_function())` to avoid computing debug output when not needed
- 📋 The base `Solver` automatically handles input copying, so parts don't interfere with each other

## 🎮 Command Line Interface

### Creating Solutions
```bash
fraocme create <day>           # Creates days/day_XX/ with solution.py and input.txt
                               # Day must be between 1 and 25 (for those calendar dates!)
```

### Running Solutions
```bash
fraocme run <day>              # Run a specific day
fraocme run 1 -p 1             # Run only part 1
fraocme run 1 --debug          # Run with debug output enabled
fraocme run 1 --no-traceback   # Hide tracebacks on errors (cleaner output)
fraocme run --all              # Run all days (marathon mode! 🏃)
```

### Viewing Statistics
```bash
fraocme stats                  # Show all stats
fraocme stats 1                # Show stats for day 1
## 🎁 Parsers & Utilities

Common parsing patterns are built right in:

```python
from fraocme.common.parser import (
    lines,      # Split into lines
    ints,       # Parse integers (one per line)
    digits,     # Parse digits into lists [[1,2,3], [4,5,6]]
    sections,   # Split by blank lines
## 🐛 Debugging

Enable debug output with the `--debug` flag:

```python
self.debug("Current value:", x)
self.debug(lambda: expensive_visualization(grid))  # Only computed when --debug is used
```

**Available Debug Helpers:**
```python
from fraocme.common.printer import (
    print_dict_row,      # Pretty-print dictionaries
    print_ranges,        # Show range summaries
## 🧪 Testing

```bash
python -m unittest discover -v tests/
# or with uv:
uv run test
```

See [tests/README.md](tests/README.md) for more details on test organization.

## 🎄 Happy Coding!

May your solutions be elegant, your bugs be few, and your stars be plentiful! ⭐⭐

---

*Built with ❤️ for Advent of Code enthusiasts*
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