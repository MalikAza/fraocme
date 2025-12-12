import math
from typing import Sequence


def sign(n: int) -> int:
    """
    Return -1, 0, or 1 based on sign of n.

    Example:
        sign(5)   Returns: 1
        sign(-3)  Returns: -1
        sign(0)   Returns: 0

    Example (moving toward target):
        current = 10
        target = 3
        step = sign(target - current)
        Returns: -1 (need to decrease)
    """
    return (n > 0) - (n < 0)


def digits(n: int) -> list[int]:
    """
    Extract digits from an integer.

    Example:
        digits(1234)
        Returns: [1, 2, 3, 4]

    Example (single digit):
        digits(7)
        Returns: [7]
    Example (use with from_digits for round-trip):
        digits(987)        Returns: [9, 8, 7]
        from_digits([9, 8, 7])  Returns: 987
    """
    return [int(d) for d in str(abs(n))]


def wrap(value: int, size: int) -> int:
    """
    Wrap value into range [0, size).

    Args:
        value: The value to wrap
        size: The size of the range (exclusive upper bound)

    Example:
        wrap(105, 100)
        Returns: 5

    Example (negative wrap):
        wrap(-10, 100)
        Returns: 90
    Example (circular position):
        position = 50
        position = wrap(position + 60, 100)
        Returns: 10  # Wrapped around
    """
    return value % size


def divisors(n: int) -> list[int]:
    """
    Get all divisors of n (including 1 and n).

    Example:
        divisors(12)
        Returns: [1, 2, 3, 4, 6, 12]

    Example:
        divisors(28)
        Returns: [1, 2, 4, 7, 14, 28]
    Example (prime number):
        divisors(17)
        Returns: [1, 17]
    """
    result = []
    sqrt_n = int(math.sqrt(n))
    for i in range(1, sqrt_n + 1):
        if n % i == 0:
            result.append(i)
            if i != n // i:
                result.append(n // i)
    return sorted(result)


def gcd(*args: int) -> int:
    """
    Greatest common divisor of multiple numbers.

    Example:
        gcd(12, 8)
        Returns: 4

    Example with multiple numbers:
        gcd(24, 36, 48)
        Returns: 12

    Common use case (simplifying fractions):
        numerator, denominator = 15, 25
        divisor = gcd(numerator, denominator)
        Returns: 5 → simplified: 3/5
    """
    result = args[0]
    for n in args[1:]:
        result = math.gcd(result, n)
    return result


def lcm(*args: int) -> int:
    """
    Least common multiple of multiple numbers.

    Example:
        lcm(4, 6)
        Returns: 12

    Example with multiple numbers:
        lcm(3, 4, 5)
        Returns: 60

    Common use case (cycle detection):
        cycles = [5, 7, 11]  # Different periods
        lcm(*cycles)
        Returns: 385  # When all cycles align
    """
    result = args[0]
    for n in args[1:]:
        result = result * n // math.gcd(result, n)
    return result


def from_digits(digits: Sequence[int]) -> int:
    """
    Combine digits back into an integer.

    Example:
        digits = [1, 2, 3, 4]
        from_digits(digits)
        Returns: 1234

    Example (reverse operation of splitting):
        digits = [9, 8, 7]
        from_digits(digits)
        Returns: 987
    """
    return int("".join(map(str, digits)))


def is_prime(n: int) -> bool:
    """
    Check if n is prime.

    Example:
        is_prime(17)
        Returns: True

    Example:
        is_prime(18)
        Returns: False

    Example (edge cases):
        is_prime(2)   Returns: True
        is_prime(1)   Returns: False
        is_prime(0)   Returns: False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_factors(n: int) -> dict[int, int]:
    """
    Get prime factorization as {prime: exponent}.

    Example:
        prime_factors(360)
        Returns: {2: 3, 3: 2, 5: 1}  # 360 = 2³ × 3² × 5

    Example:
        prime_factors(100)
        Returns: {2: 2, 5: 2}  # 100 = 2² × 5²

    Example (prime number):
        prime_factors(17)
        Returns: {17: 1}
    """
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.

    Returns (gcd, x, y) where ax + by = gcd.

    Example:
        extended_gcd(35, 15)
        Returns: (5, 1, -2)  # 35*1 + 15*(-2) = 5

    Example:
        extended_gcd(240, 46)
        Returns: (2, -9, 47)  # 240*(-9) + 46*47 = 2

    Common use case (finding modular inverse):
        g, x, _ = extended_gcd(3, 11)
        # If g == 1, then x is the modular inverse of 3 mod 11
    """
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y


def mod_inverse(a: int, m: int) -> int:
    """
    Modular multiplicative inverse: find x where (a * x) % m = 1.

    Args:
        a: Number to find inverse of
        m: Modulus

    Raises:
        ValueError: If no inverse exists (gcd(a, m) != 1)

    Example:
        mod_inverse(3, 11)
        Returns: 4  # because 3 * 4 = 12 ≡ 1 (mod 11)

    Example:
        mod_inverse(7, 26)
        Returns: 15  # because 7 * 15 = 105 ≡ 1 (mod 26)

    Common use case (cryptography, CRT):
        # Solve: 3x ≡ 5 (mod 11)
        inv = mod_inverse(3, 11)  # 4
        x = (5 * inv) % 11  # 20 % 11 = 9
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse: gcd({a}, {m}) = {g}")
    return x % m


def chinese_remainder_theorem(remainders: list[int], moduli: list[int]) -> int:
    """
    Chinese Remainder Theorem: find x where x ≡ r[i] (mod m[i]) for all i.

    Args:
        remainders: List of remainders
        moduli: List of moduli (must be pairwise coprime)

    Example:
        chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        Returns: 23  # 23 % 3 = 2, 23 % 5 = 3, 23 % 7 = 2

    Example (two equations):
        chinese_remainder_theorem([1, 4], [3, 5])
        Returns: 4  # 4 % 3 = 1, 4 % 5 = 4

    Common use case (bus schedules, cycle alignment):
        # Bus 7 departs at t=0, bus 13 departs at t=1, bus 59 departs at t=4
        # Find t where: t ≡ 0 (mod 7), t ≡ -1 (mod 13), t ≡ -4 (mod 59)
    """
    from functools import reduce

    total = 0
    m_prod = reduce(lambda a, b: a * b, moduli)

    for r, m in zip(remainders, moduli):
        mi = m_prod // m
        total += r * mi * mod_inverse(mi, m)

    return total % m_prod


def sieve_of_eratosthenes(limit: int) -> list[int]:
    """
    Generate all primes up to limit using Sieve of Eratosthenes.

    Example:
        sieve_of_eratosthenes(20)
        Returns: [2, 3, 5, 7, 11, 13, 17, 19]

    Example:
        sieve_of_eratosthenes(50)
        Returns: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

    Common use case (precompute primes for multiple queries):
        primes = sieve_of_eratosthenes(1000000)
        prime_set = set(primes)  # O(1) lookup
    """
    if limit < 2:
        return []

    is_prime_arr = [True] * (limit + 1)
    is_prime_arr[0] = is_prime_arr[1] = False

    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime_arr[i]:
            for j in range(i * i, limit + 1, i):
                is_prime_arr[j] = False

    return [i for i in range(limit + 1) if is_prime_arr[i]]


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Fast modular exponentiation: (base^exp) % mod.

    Example:
        mod_pow(2, 10, 1000)
        Returns: 24  # 2^10 = 1024, 1024 % 1000 = 24

    Example:
        mod_pow(3, 1000, 7)
        Returns: 4

    Common use case (large exponents in cryptography):
        # Compute 7^256 mod 13 without overflow
        result = mod_pow(7, 256, 13)
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result


def totient(n: int) -> int:
    """
    Euler's totient function φ(n): count of integers 1..n coprime to n.

    Example:
        totient(9)
        Returns: 6  # 1,2,4,5,7,8 are coprime to 9

    Example:
        totient(12)
        Returns: 4  # 1,5,7,11 are coprime to 12

    Example (prime):
        totient(7)
        Returns: 6  # φ(p) = p-1 for prime p
    """
    result = n
    p = 2
    temp_n = n
    while p * p <= temp_n:
        if temp_n % p == 0:
            while temp_n % p == 0:
                temp_n //= p
            result -= result // p
        p += 1
    if temp_n > 1:
        result -= result // temp_n
    return result
