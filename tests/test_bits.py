"""Tests for bit manipulation utilities."""

import pytest

from fraocme.math.binary import (
    clear_bit,
    count_bits,
    get_bit,
    int_to_binary,
    is_power_of_two,
    set_bit,
    toggle_bit,
    xor_swap,
)


class TestCountBits:
    """Tests for count_bits function."""

    def test_zero(self):
        assert count_bits(0) == 0

    def test_one(self):
        assert count_bits(1) == 1

    def test_all_ones(self):
        assert count_bits(7) == 3  # 111
        assert count_bits(15) == 4  # 1111
        assert count_bits(255) == 8  # 11111111

    def test_powers_of_two(self):
        assert count_bits(2) == 1
        assert count_bits(8) == 1
        assert count_bits(1024) == 1

    def test_mixed_bits(self):
        assert count_bits(5) == 2  # 101
        assert count_bits(10) == 2  # 1010
        assert count_bits(170) == 4  # 10101010


class TestGetBit:
    """Tests for get_bit function."""

    def test_lsb(self):
        assert get_bit(5, 0) == 1  # 101
        assert get_bit(4, 0) == 0  # 100

    def test_middle_bits(self):
        assert get_bit(5, 1) == 0  # 101
        assert get_bit(5, 2) == 1  # 101

    def test_beyond_set_bits(self):
        assert get_bit(5, 10) == 0
        assert get_bit(5, 100) == 0

    def test_negative_position_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            get_bit(5, -1)

    def test_zero(self):
        assert get_bit(0, 0) == 0
        assert get_bit(0, 5) == 0


class TestSetBit:
    """Tests for set_bit function."""

    def test_set_unset_bit(self):
        assert set_bit(5, 1) == 7  # 101 -> 111

    def test_set_already_set_bit(self):
        assert set_bit(5, 0) == 5  # 101 -> 101
        assert set_bit(5, 2) == 5  # 101 -> 101

    def test_set_from_zero(self):
        assert set_bit(0, 0) == 1
        assert set_bit(0, 3) == 8

    def test_negative_position_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            set_bit(5, -1)


class TestClearBit:
    """Tests for clear_bit function."""

    def test_clear_set_bit(self):
        assert clear_bit(7, 1) == 5  # 111 -> 101

    def test_clear_already_clear_bit(self):
        assert clear_bit(5, 1) == 5  # 101 -> 101

    def test_clear_all_bits(self):
        assert clear_bit(1, 0) == 0

    def test_negative_position_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            clear_bit(5, -1)


class TestToggleBit:
    """Tests for toggle_bit function."""

    def test_toggle_one_to_zero(self):
        assert toggle_bit(7, 1) == 5  # 111 -> 101

    def test_toggle_zero_to_one(self):
        assert toggle_bit(5, 1) == 7  # 101 -> 111

    def test_double_toggle_returns_original(self):
        original = 42
        toggled = toggle_bit(original, 3)
        assert toggle_bit(toggled, 3) == original

    def test_negative_position_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            toggle_bit(5, -1)


class TestIntToBinary:
    """Tests for int_to_binary function."""

    def test_basic_conversion(self):
        assert int_to_binary(5) == "101"
        assert int_to_binary(0) == "0"
        assert int_to_binary(1) == "1"

    def test_with_padding(self):
        assert int_to_binary(5, 8) == "00000101"
        assert int_to_binary(255, 8) == "11111111"

    def test_padding_smaller_than_number(self):
        assert int_to_binary(255, 4) == "11111111"  # No truncation

    def test_negative_with_width(self):
        assert int_to_binary(-1, 8) == "11111111"
        assert int_to_binary(-1, 4) == "1111"


class TestIsPowerOfTwo:
    """Tests for is_power_of_two function."""

    def test_powers_of_two(self):
        assert is_power_of_two(1) is True  # 2^0
        assert is_power_of_two(2) is True
        assert is_power_of_two(4) is True
        assert is_power_of_two(8) is True
        assert is_power_of_two(1024) is True

    def test_not_powers_of_two(self):
        assert is_power_of_two(0) is False
        assert is_power_of_two(3) is False
        assert is_power_of_two(6) is False
        assert is_power_of_two(10) is False

    def test_negative_numbers(self):
        assert is_power_of_two(-1) is False
        assert is_power_of_two(-2) is False


class TestXorSwap:
    """Tests for xor_swap function."""

    def test_basic_swap(self):
        assert xor_swap(5, 10) == (10, 5)

    def test_swap_with_zero(self):
        assert xor_swap(0, 5) == (5, 0)

    def test_same_values(self):
        assert xor_swap(5, 5) == (5, 5)

    def test_negative_numbers(self):
        assert xor_swap(-3, 7) == (7, -3)
