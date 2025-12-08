class Colors:
    """ANSI color codes."""

    # Reset
    RESET = "\033[0m"

    # Regular colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"

    # Bright colors
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_MAGENTA = "\033[95m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"


class c:  # noqa: N801
    """
    Short color formatting helpers.

    Usage:
        print(c.green("Success!"))
        print(c.red("Error!"))
        print(c.bold(c.cyan("Important")))
    """

    @staticmethod
    def _wrap(color: str, text: str) -> str:
        return f"{color}{text}{Colors.RESET}"

    # Basic colors
    @staticmethod
    def red(text: str) -> str:
        return c._wrap(Colors.RED, text)

    @staticmethod
    def green(text: str) -> str:
        return c._wrap(Colors.GREEN, text)

    @staticmethod
    def yellow(text: str) -> str:
        return c._wrap(Colors.YELLOW, text)

    @staticmethod
    def cyan(text: str) -> str:
        return c._wrap(Colors.CYAN, text)

    @staticmethod
    def magenta(text: str) -> str:
        return c._wrap(Colors.MAGENTA, text)

    # Styles
    @staticmethod
    def bold(text: str) -> str:
        return c._wrap(Colors.BOLD, text)

    @staticmethod
    def dim(text: str) -> str:
        return c._wrap(Colors.DIM, text)

    # Semantic colors
    @staticmethod
    def success(text: str) -> str:
        return c._wrap(Colors.BRIGHT_GREEN, text)

    @staticmethod
    def error(text: str) -> str:
        return c._wrap(Colors.BRIGHT_RED, text)

    @staticmethod
    def warning(text: str) -> str:
        return c._wrap(Colors.BRIGHT_YELLOW, text)

    @staticmethod
    def info(text: str) -> str:
        return c._wrap(Colors.BRIGHT_CYAN, text)

    @staticmethod
    def muted(text: str) -> str:
        return c.dim(text)

    # Stats coloring
    @staticmethod
    def stat(
        val: int | float,
        min_val: int | float,
        max_val: int | float,
        median_val: int | float,
    ) -> str:
        """
        Color a value based on its position in the dataset.
        - Green: maximum
        - Red: minimum
        - Yellow: median
        - Muted: other
        """
        if isinstance(val, float) and not val.is_integer():
            text = f"{val:.2f}"
        else:
            text = str(int(val) if isinstance(val, float) else val)

        if val == max_val:
            return c.green(text)
        elif val == min_val:
            return c.red(text)
        elif val == median_val:
            return c.yellow(text)
        return c.muted(text)

    # Time formatting (for solver output)
    @staticmethod
    def time(ms: float) -> str:
        """Color time based on performance."""
        formatted = f"({ms:.2f}ms)"
        if ms < 100:
            return c._wrap(Colors.BRIGHT_GREEN, formatted)
        elif ms < 1000:
            return c._wrap(Colors.BRIGHT_YELLOW, formatted)
        else:
            return c._wrap(Colors.BRIGHT_RED, formatted)
