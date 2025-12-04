# Tests

Comprehensive test suite for the `fraocme` project using Python's `unittest` framework.

## Running Tests

### Using uv (recommended)

```bash
# Run all tests using the project's test command
uv run tests

# Run all tests with verbose output (direct discovery)
uv run python -m unittest discover tests -v

# Run specific test file
uv run python -m unittest tests.test_core -v

# Run specific test class
uv run python -m unittest tests.test_core.TestSolver -v

# Run specific test method
uv run python -m unittest tests.test_core.TestSolver.test_solver_initialization -v
```

The primary command is `uv run tests` which uses the test runner configured in `pyproject.toml`.



### Using pytest (optional)

```bash
# Install dev dependencies
uv sync --extra dev

# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=fraocme --cov-report=html
```

### Direct Python (without uv)

```bash
# Run all tests
python -m unittest discover tests -v

# Run specific file
python -m unittest tests.test_core
```

## Test Organization

### `test_cli.py`
Tests for the `fraocme.cli` module:
- **MainArgumentParsing**: CLI argument parsing with argparse
  - Command routing (run, stats)
  - Flag handling (--all, --debug, --part, --no-stats)
- **CmdRun**: Run command handler
  - Running specific days
  - Running all days
  - Part selection
- **CmdStats**: Stats command handler
  - Displaying statistics for days
  - Best-only filtering

### `test_core.py`
Tests for the `fraocme.core` module:
- **Solver**: Base class for solutions
  - Initialization and configuration
  - Input loading and parsing
  - Abstract method enforcement
- **Runner**: Discovers and executes solver solutions
  - Day discovery and validation
  - Module loading and instantiation
  - Solver execution with parts

### `test_debug.py`
Tests for the `fraocme.debug` module:
- **Colors**: ANSI color codes and styles
- **ColorHelper (c)**: Color formatting utility functions
  - `c.red()`, `c.green()`, `c.blue()`, etc.
  - `c.bold()`, `c.cyan()`, etc.
- **Printing Functions**:
  - `print_header()` - formatted headers with lines
  - `print_section()` - section dividers
  - `print_grid()` - 2D grid display with separators
  - `print_max_in_rows()` - max value per row

### `test_ui.py`
Tests for the `fraocme.ui` module:
- **Colors**: ANSI color code constants and helper class
- **ColorHelper (c)**: Semantic color methods
  - Color functions: `red()`, `green()`, `blue()`, etc.
  - Style functions: `bold()`, `italic()`, `underline()`
  - Semantic colors: `success()`, `error()`, `warning()`, `info()`
  - Time formatting: `time()` with performance-based coloring
- **Printer Functions**:
  - `print_header()` - headers with box drawing characters
  - `print_section()` - section dividers

### `test_common.py`
Tests for the `fraocme.common` module:
- **Printer**: Common printing utilities
  - `print_max_in_rows()` - display maximum value per row

### `test_grid.py`
Tests for the `fraocme.grid` module:
- **Parser**: Grid parsing utilities
  - `lines()` - parse lines from raw string
  - `int_grid()` - parse 2D grid of single digits
- **Printer**: Grid display utilities
  - `print_grid()` - display 2D grids with optional highlighting
- **GridUtils**: Utility class for grid navigation
  - Position checking: `is_position_out_of_bounds()`
  - Direction movement: `get_position_up/down/left/right()`
  - Diagonal movement: `get_position_diagonal()`
  - Multi-position retrieval: `get_positions_around()`, `get_positions_in_nsew()`, `get_positions_in_corners()`
  - Value operations: `search_value()`, `get_cell_value()`
  - Start/end position tracking

### `test_profiling.py`
Tests for the `fraocme.profiling` module:
- **Timer**: Benchmarking with lap tracking
  - `start()`, `stop()`, `lap()`
  - Statistics: `total`, `average`, `min`, `max`
- **Decorators**:
  - `@timed` - prints execution time
  - `@benchmark` - runs multiple iterations with stats
- **Stats**: Track and display solution statistics
  - `update()` - record part results
  - `save()`/`load()` - persistence
  - `print_day()`, `print_all()` - formatted output

## Test Coverage

The test suite provides comprehensive coverage of:
- ✅ CLI argument parsing and command handling
- ✅ Core solver and runner functionality
- ✅ Grid utilities and navigation
- ✅ UI/color formatting utilities
- ✅ Performance profiling tools
- ✅ Edge cases and error handling

## Adding New Tests

1. Create test files named `test_*.py` in the `tests/` directory
2. Use unittest classes inheriting from `unittest.TestCase`
3. Name test methods starting with `test_`
4. Use descriptive docstrings for test documentation

Example:
```python
import unittest

class TestMyModule(unittest.TestCase):
    """Test MyModule functionality."""
    
    def test_example(self):
        """Test example function."""
        result = my_function(5)
        self.assertEqual(result, 10)
```

## Dependencies

Tests require only Python's built-in `unittest` module.

Optional dependencies for enhanced testing:
- `pytest` - Alternative test runner with advanced features
- `pytest-cov` - Coverage reporting

Install with:
```bash
uv pip install pytest pytest-cov
```

## Configuration

Test configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
```

## Tips

- Use `setUp()` and `tearDown()` for test fixtures
- Test both success and error cases
- Use descriptive test names and docstrings
- Keep tests independent and repeatable
- Mock external dependencies when needed
