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
uv run python -m unittest tests.test_parsers -v

# Run specific test class
uv run python -m unittest tests.test_parsers.TestBasicParsers -v

# Run specific test method
uv run python -m unittest tests.test_parsers.TestBasicParsers.test_lines -v
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
python -m unittest tests.test_parsers
```

## Test Organization

### `test_parsers.py`
Tests for the `fraocme.parsers` module:
- **BasicParsers**: `lines()`, `ints()`, `floats()`, `ints_per_line()`
- **WordParsers**: `words()` function for extracting alphabetic words
- **BlockParsers**: `blocks()` for splitting by delimiters
- **CSVParsers**: `csv()` and `csv_ints()` for parsing comma-separated values
- **GridParsers**: `char_grid()` and `int_grid()` for 2D grids
- **MappedParsers**: `mapped()` for custom line parsers

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
- ✅ Input parsing for various formats
- ✅ Core solver and runner functionality
- ✅ Debug/console formatting utilities
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
