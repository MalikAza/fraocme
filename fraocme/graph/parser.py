from typing import Callable, TypeVar

K = TypeVar("K")
V = TypeVar("V")


def parse_adjacency_list(
    raw: str,
    separator: str = ": ",
    value_separator: str | None = None,
    key_type: Callable[[str], K] = str,
    value_type: Callable[[str], V] = str,
) -> dict[K, list[V]]:
    """
    Parse adjacency list or key-value format

    Args:
        raw: Raw input string
        separator: Separator between key and values (default: ": ")
        value_separator: Separator between values (default: None).
            When `None`, uses whitespace and commas as separators.
        key_type: Type conversion for keys (default: str)
        value_type: Type conversion for values (default: str)

    Examples:
        Adjacency list (strings, auto-detect):
        >>> parse_adjacency_list("aaa: bbb ccc\\nbbb: ddd")
        {'aaa': ['bbb', 'ccc'], 'bbb': ['ddd']}

        Comma-separated values:
        >>> parse_adjacency_list("aaa: bbb, ccc\\nbbb: ddd")
        {'aaa': ['bbb', 'ccc'], 'bbb': ['ddd']}

        Explicit value separator:
        >>> parse_adjacency_list("aaa: bbb,ccc\\nbbb: ddd", value_separator=",")
        {'aaa': ['bbb', 'ccc'], 'bbb': ['ddd']}

        Custom separator:
        >>> parse_adjacency_list("A -> B, C\\nB -> D", separator=" -> ")
        {'A': ['B', 'C'], 'B': ['D']}

        Key with integers:
        >>> parse_adjacency_list(
        ...     "190: 10 19\\n3267: 81 40 27",
        ...     key_type=int,
        ...     value_type=int,
        ... )
        {190: [10, 19], 3267: [81, 40, 27]}
    """
    result: dict[K, list[V]] = {}
    for line in raw.strip().splitlines():
        if separator not in line:
            continue
        key_str, values_str = line.split(separator, 1)
        key = key_type(key_str.strip())

        if values_str.strip() == "":
            vals: list[V] = []
        else:
            if value_separator is not None:
                # Use explicit separator
                vals = [
                    value_type(v.strip())
                    for v in values_str.split(value_separator)
                    if v.strip()
                ]
            else:
                # Auto-detect: handle both space and comma separated values
                values_str = values_str.replace(",", " ")
                vals = [value_type(v.strip()) for v in values_str.split() if v.strip()]

        result[key] = vals
    return result
