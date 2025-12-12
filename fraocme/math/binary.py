def count_bits(n: int) -> int:
    """
    Count the number of set bits (1s) in an integer (population count / Hamming weight).

    Args:
        n: Integer to count bits in (handles negative via two's complement)

    Returns:
        Number of 1-bits in the binary representation

    Example (basic):
        count_bits(7)  # binary: 111
        Returns: 3

    Example (power of 2):
        count_bits(8)  # binary: 1000
        Returns: 1

    Example (zero):
        count_bits(0)
        Returns: 0

    Example (larger number):
        count_bits(255)  # binary: 11111111
        Returns: 8
    """
    return bin(n).count("1")


def get_bit(n: int, position: int) -> int:
    """
    Get the bit value at a specific position (0-indexed from right).

    Args:
        n: Integer to extract bit from
        position: Bit position (0 = least significant bit)

    Returns:
        0 or 1 depending on bit value

    Raises:
        ValueError: If position is negative

    Example (LSB):
        get_bit(5, 0)  # binary: 101, position 0
        Returns: 1

    Example (middle bit):
        get_bit(5, 1)  # binary: 101, position 1
        Returns: 0

    Example (MSB of small number):
        get_bit(5, 2)  # binary: 101, position 2
        Returns: 1

    Example (beyond set bits):
        get_bit(5, 10)  # binary: 101, position 10
        Returns: 0
    """
    if position < 0:
        raise ValueError(f"Position must be non-negative: got {position}")
    return (n >> position) & 1


def set_bit(n: int, position: int) -> int:
    """
    Set the bit at a specific position to 1.

    Args:
        n: Original integer
        position: Bit position to set (0 = least significant bit)

    Returns:
        Integer with the specified bit set to 1

    Raises:
        ValueError: If position is negative

    Example (set unset bit):
        set_bit(5, 1)  # binary: 101 -> 111
        Returns: 7

    Example (set already set bit):
        set_bit(5, 0)  # binary: 101 -> 101
        Returns: 5

    Example (set high bit):
        set_bit(0, 3)  # binary: 0 -> 1000
        Returns: 8
    """
    if position < 0:
        raise ValueError(f"Position must be non-negative: got {position}")
    return n | (1 << position)


def clear_bit(n: int, position: int) -> int:
    """
    Clear the bit at a specific position (set to 0).

    Args:
        n: Original integer
        position: Bit position to clear (0 = least significant bit)

    Returns:
        Integer with the specified bit set to 0

    Raises:
        ValueError: If position is negative

    Example (clear set bit):
        clear_bit(7, 1)  # binary: 111 -> 101
        Returns: 5

    Example (clear already clear bit):
        clear_bit(5, 1)  # binary: 101 -> 101
        Returns: 5
    """
    if position < 0:
        raise ValueError(f"Position must be non-negative: got {position}")
    return n & ~(1 << position)


def toggle_bit(n: int, position: int) -> int:
    """
    Toggle the bit at a specific position (flip 0↔1).

    Args:
        n: Original integer
        position: Bit position to toggle (0 = least significant bit)

    Returns:
        Integer with the specified bit flipped

    Raises:
        ValueError: If position is negative

    Example (toggle 1 to 0):
        toggle_bit(7, 1)  # binary: 111 -> 101
        Returns: 5

    Example (toggle 0 to 1):
        toggle_bit(5, 1)  # binary: 101 -> 111
        Returns: 7
    """
    if position < 0:
        raise ValueError(f"Position must be non-negative: got {position}")
    return n ^ (1 << position)


def int_to_binary(n: int, width: int | None = None) -> str:
    """
    Convert integer to binary string representation.

    Args:
        n: Integer to convert
        width: Optional minimum width (zero-padded)

    Returns:
        Binary string (without '0b' prefix)

    Example (basic):
        int_to_binary(5)
        Returns: '101'

    Example (with padding):
        int_to_binary(5, 8)
        Returns: '00000101'

    Example (byte representation):
        int_to_binary(255, 8)
        Returns: '11111111'

    Example (negative - shows two's complement):
        int_to_binary(-1, 8)
        Returns: '11111111'
    """
    if n < 0 and width:
        # Two's complement for negative numbers
        return format(n & ((1 << width) - 1), f"0{width}b")
    if width:
        return format(n, f"0{width}b")
    return bin(n)[2:] if n >= 0 else bin(n)[3:]


def is_power_of_two(n: int) -> bool:
    """
    Check if a number is a power of two.

    Args:
        n: Integer to check

    Returns:
        True if n is a power of 2, False otherwise

    Example (powers of 2):
        is_power_of_two(8)   # 2³
        Returns: True

    Example (not power of 2):
        is_power_of_two(6)
        Returns: False

    Example (edge cases):
        is_power_of_two(0)
        Returns: False
        is_power_of_two(1)  # 2⁰
        Returns: True
    """
    return n > 0 and (n & (n - 1)) == 0


def xor_swap(a: int, b: int) -> tuple[int, int]:
    """
    Swap two integers using XOR (demonstration of XOR properties).

    Args:
        a: First integer
        b: Second integer

    Returns:
        Tuple of (b, a) - values swapped

    Example:
        xor_swap(5, 10)
        Returns: (10, 5)

    Note:
        In practice, Python's tuple unpacking (a, b = b, a) is preferred.
        This demonstrates the XOR swap algorithm.
    """
    if a != b:  # XOR swap fails when a and b reference same value
        a = a ^ b
        b = a ^ b
        a = a ^ b
    return a, b
