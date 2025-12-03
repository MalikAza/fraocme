from typing import TypeVar, Callable

T = TypeVar('T')


# ─────────────────────────────────────────────────────────
# Basic parsers
# ─────────────────────────────────────────────────────────

def lines(raw: str) -> list[str]:
    """
    Parse input as list of strings (one per line).
    
    Example:
        "hello\\nworld" -> ["hello", "world"]
    """
    return raw.strip().split('\n')


def ints(raw: str) -> list[int]:
    """
    Parse input as list of integers (one per line).
    
    Example:
        "42\\n100\\n-5" -> [42, 100, -5]
    """
    return [int(line) for line in lines(raw)]


def ints_per_line(raw: str, delimiter: str | None = None) -> list[list[int]]:
    """
    Parse input as lists of integers per line.
    
    Args:
        delimiter: Separator between numbers (default: whitespace)
    
    Example:
        "1 2 3\\n4 5 6" -> [[1, 2, 3], [4, 5, 6]]
    """
    return [list(map(int, line.split(delimiter))) for line in lines(raw)]


def floats(raw: str) -> list[float]:
    """
    Parse input as list of floats (one per line).
    
    Example:
        "3.14\\n2.71" -> [3.14, 2.71]
    """
    return [float(line) for line in lines(raw)]


def words(raw: str) -> list[str]:
    """
    Extract all alphabetic words from input.
    
    Example:
        "hello 123 world" -> ["hello", "world"]
    """
    return re.findall(r'[a-zA-Z]+', raw)


# ─────────────────────────────────────────────────────────
# Block parsers
# ─────────────────────────────────────────────────────────

def blocks(raw: str, delimiter: str = '\n\n') -> list[str]:
    """
    Parse input separated by blank lines.
    
    Example:
        "line1\\nline2\\n\\nline3" -> ["line1\\nline2", "line3"]
    """
    return raw.strip().split(delimiter)


# ─────────────────────────────────────────────────────────
# CSV parsers
# ─────────────────────────────────────────────────────────

def csv(raw: str, delimiter: str = ',') -> list[str]:
    """
    Parse single line CSV input.
    
    Example:
        "apple,banana,cherry" -> ["apple", "banana", "cherry"]
    """
    return [x.strip() for x in raw.strip().split(delimiter)]


def csv_ints(raw: str, delimiter: str = ',') -> list[int]:
    """
    Parse single line CSV of integers.
    
    Example:
        "10,20,30" -> [10, 20, 30]
    """
    return [int(x.strip()) for x in raw.strip().split(delimiter)]


# ─────────────────────────────────────────────────────────
# Grid parsers
# ─────────────────────────────────────────────────────────

def char_grid(raw: str) -> list[list[str]]:
    """
    Parse input as 2D grid of characters.
    
    Example:
        "abc\\ndef" -> [['a','b','c'], ['d','e','f']]
    """
    return [[char for char in line] for line in lines(raw)]


def int_grid(raw: str) -> list[list[int]]:
    """
    Parse input as 2D grid of single digits.
    
    Example:
        "123\\n456" -> [[1,2,3], [4,5,6]]
    """
    return [[int(char) for char in line] for line in lines(raw)]




# ─────────────────────────────────────────────────────────
# Custom mapper
# ─────────────────────────────────────────────────────────

def mapped(raw: str, line_parser: Callable[[str], T]) -> list[T]:
    """
    Parse each line with a custom parser function.
    
    Example:
        def parse_game(line):
            parts = line.split()
            return (parts[0], int(parts[1]))
        
        data = mapped(raw, parse_game)
    """
    return [line_parser(line) for line in lines(raw)]