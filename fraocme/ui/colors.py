# TODO: there is maybe too much?? (thanks copilot)
class Colors:
    """ANSI color codes."""

    # Reset
    RESET = "\033[0m"

    # Regular colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"


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

    # Regular colors
    @staticmethod
    def black(text: str) -> str:
        return c._wrap(Colors.BLACK, text)

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
    def blue(text: str) -> str:
        return c._wrap(Colors.BLUE, text)

    @staticmethod
    def magenta(text: str) -> str:
        return c._wrap(Colors.MAGENTA, text)

    @staticmethod
    def cyan(text: str) -> str:
        return c._wrap(Colors.CYAN, text)

    @staticmethod
    def white(text: str) -> str:
        return c._wrap(Colors.WHITE, text)

    # Bright colors
    @staticmethod
    def bright_red(text: str) -> str:
        return c._wrap(Colors.BRIGHT_RED, text)

    @staticmethod
    def bright_green(text: str) -> str:
        return c._wrap(Colors.BRIGHT_GREEN, text)

    @staticmethod
    def bright_yellow(text: str) -> str:
        return c._wrap(Colors.BRIGHT_YELLOW, text)

    @staticmethod
    def bright_blue(text: str) -> str:
        return c._wrap(Colors.BRIGHT_BLUE, text)

    @staticmethod
    def bright_cyan(text: str) -> str:
        return c._wrap(Colors.BRIGHT_CYAN, text)

    # Styles
    @staticmethod
    def bold(text: str) -> str:
        return c._wrap(Colors.BOLD, text)

    @staticmethod
    def dim(text: str) -> str:
        return c._wrap(Colors.DIM, text)

    @staticmethod
    def italic(text: str) -> str:
        return c._wrap(Colors.ITALIC, text)

    @staticmethod
    def underline(text: str) -> str:
        return c._wrap(Colors.UNDERLINE, text)

    # Semantic colors
    @staticmethod
    def success(text: str) -> str:
        return c.bright_green(text)

    @staticmethod
    def error(text: str) -> str:
        return c.bright_red(text)

    @staticmethod
    def warning(text: str) -> str:
        return c.bright_yellow(text)

    @staticmethod
    def info(text: str) -> str:
        return c.bright_cyan(text)

    @staticmethod
    def muted(text: str) -> str:
        return c.dim(text)

    # Time formatting (for solver output)
    @staticmethod
    def time(ms: float) -> str:
        """Color time based on performance."""
        formatted = f"({ms:.2f}ms)"
        if ms < 100:
            return c.bright_green(formatted)
        elif ms < 1000:
            return c.bright_yellow(formatted)
        else:
            return c.bright_red(formatted)

    # Custom
    @staticmethod
    def custom(text: str, *codes: str) -> str:
        """Apply multiple color codes."""
        prefix = "".join(codes)
        return f"{prefix}{text}{Colors.RESET}"
