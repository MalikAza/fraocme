import unittest

from fraocme.math.geometry import (
    euclidean_distance,
    squared_euclidean_distance,
)
from fraocme.math.number_theory import (
    chinese_remainder_theorem,
    digits,
    divisors,
    extended_gcd,
    from_digits,
    gcd,
    is_prime,
    lcm,
    mod_inverse,
    mod_pow,
    prime_factors,
    sieve_of_eratosthenes,
    sign,
    totient,
    wrap,
)


class TestMathHelpers(unittest.TestCase):
    def test_sign_digits_wrap(self):
        self.assertEqual(sign(5), 1)
        self.assertEqual(sign(-3), -1)
        self.assertEqual(sign(0), 0)
        self.assertEqual(digits(-987), [9, 8, 7])
        self.assertEqual(wrap(105, 100), 5)
        self.assertEqual(wrap(-10, 100), 90)

    def test_number_theory_helpers(self):
        self.assertEqual(divisors(12), [1, 2, 3, 4, 6, 12])
        self.assertEqual(gcd(24, 36, 18), 6)
        self.assertEqual(lcm(3, 4, 5), 60)
        self.assertEqual(from_digits([9, 8, 7]), 987)

    def test_euclidean_distance_2d(self):
        # Basic 3-4-5 triangle
        self.assertEqual(euclidean_distance((0, 0), (3, 4)), 5.0)
        # Same point
        self.assertEqual(euclidean_distance((5, 5), (5, 5)), 0.0)
        # With floats
        self.assertEqual(euclidean_distance((1.5, 2.5), (4.5, 6.5)), 5.0)

    def test_euclidean_distance_3d(self):
        dist = euclidean_distance((162, 817, 812), (57, 618, 57))
        self.assertAlmostEqual(dist, 787.814064, places=5)

        dist2 = euclidean_distance((162, 817, 812), (906, 360, 560))
        self.assertAlmostEqual(dist2, 908.784353, places=5)

    def test_euclidean_distance_different_dimensions(self):
        with self.assertRaises(ValueError) as context:
            euclidean_distance((1, 2), (1, 2, 3))
        self.assertIn("same dimensions", str(context.exception))

    def test_squared_euclidean_distance_2d(self):
        self.assertEqual(squared_euclidean_distance((0, 0), (3, 4)), 25.0)
        self.assertEqual(squared_euclidean_distance((5, 5), (5, 5)), 0.0)

    def test_squared_euclidean_distance_3d(self):
        sq_dist = squared_euclidean_distance((162, 817, 812), (57, 618, 57))
        self.assertEqual(sq_dist, 620651.0)

    def test_squared_euclidean_distance_comparison(self):
        box1 = (162, 817, 812)
        box2 = (57, 618, 57)
        box3 = (906, 360, 560)

        dist_to_box2 = squared_euclidean_distance(box1, box2)
        dist_to_box3 = squared_euclidean_distance(box1, box3)

        self.assertLess(dist_to_box2, dist_to_box3)

    def test_squared_euclidean_distance_different_dimensions(self):
        with self.assertRaises(ValueError) as context:
            squared_euclidean_distance((1, 2), (1, 2, 3))
        self.assertIn("same dimensions", str(context.exception))


class TestPrimes(unittest.TestCase):
    def test_is_prime_basic(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(11))
        self.assertTrue(is_prime(13))
        self.assertTrue(is_prime(17))
        self.assertTrue(is_prime(19))

    def test_is_prime_not_prime(self):
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(100))

    def test_is_prime_large(self):
        self.assertTrue(is_prime(104729))  # 10000th prime
        self.assertFalse(is_prime(104730))

    def test_prime_factors_basic(self):
        self.assertEqual(prime_factors(12), {2: 2, 3: 1})  # 12 = 2² × 3
        self.assertEqual(prime_factors(360), {2: 3, 3: 2, 5: 1})  # 360 = 2³ × 3² × 5
        self.assertEqual(prime_factors(100), {2: 2, 5: 2})  # 100 = 2² × 5²

    def test_prime_factors_prime(self):
        self.assertEqual(prime_factors(17), {17: 1})
        self.assertEqual(prime_factors(2), {2: 1})

    def test_prime_factors_power_of_prime(self):
        self.assertEqual(prime_factors(8), {2: 3})  # 8 = 2³
        self.assertEqual(prime_factors(27), {3: 3})  # 27 = 3³

    def test_sieve_of_eratosthenes_small(self):
        self.assertEqual(sieve_of_eratosthenes(10), [2, 3, 5, 7])
        self.assertEqual(sieve_of_eratosthenes(20), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_sieve_of_eratosthenes_edge_cases(self):
        self.assertEqual(sieve_of_eratosthenes(0), [])
        self.assertEqual(sieve_of_eratosthenes(1), [])
        self.assertEqual(sieve_of_eratosthenes(2), [2])

    def test_sieve_of_eratosthenes_count(self):
        primes = sieve_of_eratosthenes(100)
        self.assertEqual(len(primes), 25)  # 25 primes below 100


class TestModularArithmetic(unittest.TestCase):
    def test_extended_gcd_basic(self):
        g, x, y = extended_gcd(35, 15)
        self.assertEqual(g, 5)
        self.assertEqual(35 * x + 15 * y, 5)

    def test_extended_gcd_coprime(self):
        g, x, y = extended_gcd(3, 11)
        self.assertEqual(g, 1)
        self.assertEqual(3 * x + 11 * y, 1)

    def test_extended_gcd_with_zero(self):
        g, x, y = extended_gcd(5, 0)
        self.assertEqual(g, 5)
        self.assertEqual(x, 1)
        self.assertEqual(y, 0)

    def test_mod_inverse_basic(self):
        # 3 * 4 = 12 ≡ 1 (mod 11)
        self.assertEqual(mod_inverse(3, 11), 4)
        # Verify: (3 * result) % 11 == 1
        self.assertEqual((3 * mod_inverse(3, 11)) % 11, 1)

    def test_mod_inverse_various(self):
        # 7 * 15 = 105 ≡ 1 (mod 26)
        self.assertEqual((7 * mod_inverse(7, 26)) % 26, 1)
        # 17 * ? ≡ 1 (mod 43)
        self.assertEqual((17 * mod_inverse(17, 43)) % 43, 1)

    def test_mod_inverse_no_inverse(self):
        with self.assertRaises(ValueError):
            mod_inverse(2, 4)  # gcd(2, 4) = 2 ≠ 1

    def test_mod_pow_basic(self):
        # 2^10 = 1024, 1024 % 1000 = 24
        self.assertEqual(mod_pow(2, 10, 1000), 24)
        self.assertEqual(mod_pow(3, 5, 7), 5)  # 3^5 = 243, 243 % 7 = 5

    def test_mod_pow_large_exponent(self):
        # Should handle large exponents without overflow
        result = mod_pow(2, 1000, 1000000007)
        self.assertIsInstance(result, int)
        self.assertLess(result, 1000000007)

    def test_mod_pow_edge_cases(self):
        self.assertEqual(mod_pow(5, 0, 13), 1)  # x^0 = 1
        self.assertEqual(mod_pow(0, 5, 13), 0)  # 0^x = 0
        self.assertEqual(mod_pow(7, 1, 13), 7)  # x^1 = x


class TestChineseRemainderTheorem(unittest.TestCase):
    def test_crt_basic(self):
        # x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
        result = chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
        self.assertEqual(result % 3, 2)
        self.assertEqual(result % 5, 3)
        self.assertEqual(result % 7, 2)
        self.assertEqual(result, 23)

    def test_crt_two_equations(self):
        # x ≡ 1 (mod 3), x ≡ 4 (mod 5)
        result = chinese_remainder_theorem([1, 4], [3, 5])
        self.assertEqual(result % 3, 1)
        self.assertEqual(result % 5, 4)
        self.assertEqual(result, 4)

    def test_crt_larger_moduli(self):
        # x ≡ 0 (mod 7), x ≡ 12 (mod 13), x ≡ 58 (mod 59)
        result = chinese_remainder_theorem([0, 12, 58], [7, 13, 59])
        self.assertEqual(result % 7, 0)
        self.assertEqual(result % 13, 12)
        self.assertEqual(result % 59, 58)


class TestTotient(unittest.TestCase):
    def test_totient_prime(self):
        # φ(p) = p - 1 for prime p
        self.assertEqual(totient(7), 6)
        self.assertEqual(totient(11), 10)
        self.assertEqual(totient(13), 12)

    def test_totient_prime_power(self):
        # φ(p^k) = p^k - p^(k-1)
        self.assertEqual(totient(8), 4)  # φ(2³) = 8 - 4 = 4
        self.assertEqual(totient(9), 6)  # φ(3²) = 9 - 3 = 6

    def test_totient_composite(self):
        self.assertEqual(totient(12), 4)  # 1, 5, 7, 11
        self.assertEqual(totient(10), 4)  # 1, 3, 7, 9

    def test_totient_small_values(self):
        self.assertEqual(totient(1), 1)
        self.assertEqual(totient(2), 1)
        self.assertEqual(totient(3), 2)
        self.assertEqual(totient(4), 2)
        self.assertEqual(totient(5), 4)
        self.assertEqual(totient(6), 2)


if __name__ == "__main__":
    unittest.main()
