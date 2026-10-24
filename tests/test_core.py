"""Tests for roman_numerals_utils.core.

All tests are deterministic and cover the edge cases the implementation
actually claims to handle, per the documented scope.
"""

import unittest

from roman_numerals_utils import RomanError, from_roman, to_roman


class TestToRomanHappyPath(unittest.TestCase):
    """Verify correct conversion for in-range integers."""

    def test_one(self):
        self.assertEqual(to_roman(1), "I")

    def test_two(self):
        self.assertEqual(to_roman(2), "II")

    def test_three(self):
        self.assertEqual(to_roman(3), "III")

    def test_four(self):
        self.assertEqual(to_roman(4), "IV")

    def test_five(self):
        self.assertEqual(to_roman(5), "V")

    def test_nine(self):
        self.assertEqual(to_roman(9), "IX")

    def test_forty(self):
        self.assertEqual(to_roman(40), "XL")

    def test_forty_nine(self):
        self.assertEqual(to_roman(49), "XLIX")

    def test_ninety(self):
        self.assertEqual(to_roman(90), "XC")

    def test_four_hundred(self):
        self.assertEqual(to_roman(400), "CD")

    def test_nine_hundred(self):
        self.assertEqual(to_roman(900), "CM")

    def test_max(self):
        self.assertEqual(to_roman(3999), "MMMCMXCIX")

    def test_round_numbers(self):
        self.assertEqual(to_roman(1000), "M")
        self.assertEqual(to_roman(2000), "MM")
        self.assertEqual(to_roman(3000), "MMM")


class TestToRomanRejection(unittest.TestCase):
    """Verify that out-of-range and wrong-type inputs raise RomanError."""

    def test_zero(self):
        with self.assertRaises(RomanError):
            to_roman(0)

    def test_negative(self):
        with self.assertRaises(RomanError):
            to_roman(-1)

    def test_too_large(self):
        with self.assertRaises(RomanError):
            to_roman(4000)

    def test_bool_rejected(self):
        # bool is a subclass of int; we reject it explicitly so that
        # to_roman(True) does not silently produce "I".
        with self.assertRaises(RomanError):
            to_roman(True)

    def test_float_rejected(self):
        with self.assertRaises(RomanError):
            to_roman(3.0)

    def test_string_rejected(self):
        with self.assertRaises(RomanError):
            to_roman("5")

    def test_none_rejected(self):
        with self.assertRaises(RomanError):
            to_roman(None)


class TestFromRomanHappyPath(unittest.TestCase):
    """Verify correct parsing of canonical numerals."""

    def test_one(self):
        self.assertEqual(from_roman("I"), 1)

    def test_four(self):
        self.assertEqual(from_roman("IV"), 4)

    def test_nine(self):
        self.assertEqual(from_roman("IX"), 9)

    def test_forty_nine(self):
        self.assertEqual(from_roman("XLIX"), 49)

    def test_max(self):
        self.assertEqual(from_roman("MMMCMXCIX"), 3999)

    def test_round_trips(self):
        self.assertEqual(from_roman("M"), 1000)
        self.assertEqual(from_roman("MM"), 2000)
        self.assertEqual(from_roman("MMM"), 3000)


class TestFromRomanRejection(unittest.TestCase):
    """Verify that invalid inputs raise RomanError."""

    def test_empty_string(self):
        with self.assertRaises(RomanError):
            from_roman("")

    def test_whitespace_only(self):
        with self.assertRaises(RomanError):
            from_roman("   ")

    def test_leading_whitespace(self):
        with self.assertRaises(RomanError):
            from_roman(" IV")

    def test_trailing_whitespace(self):
        with self.assertRaises(RomanError):
            from_roman("IV ")

    def test_lowercase(self):
        with self.assertRaises(RomanError):
            from_roman("iv")

    def test_invalid_char(self):
        with self.assertRaises(RomanError):
            from_roman("XIZ")

    def test_non_canonical_iiii(self):
        # IIII = 4, but not canonical (should be IV).
        with self.assertRaises(RomanError):
            from_roman("IIII")

    def test_non_canonical_vv(self):
        # VV = 10, but not canonical (should be X).
        with self.assertRaises(RomanError):
            from_roman("VV")

    def test_non_canonical_ic(self):
        # IC parses to 99 via subtractive rule, but canonical is XCIX.
        with self.assertRaises(RomanError):
            from_roman("IC")

    def test_non_string(self):
        with self.assertRaises(RomanError):
            from_roman(5)

    def test_none(self):
        with self.assertRaises(RomanError):
            from_roman(None)


class TestRoundTrip(unittest.TestCase):
    """Verify to_roman and from_roman are mutual inverses."""

    def test_all_values_round_trip(self):
        for n in range(1, 4000):
            with self.subTest(n=n):
                self.assertEqual(from_roman(to_roman(n)), n)

    def test_canonical_strings_round_trip(self):
        # Every string produced by to_roman must be accepted by from_roman.
        for n in range(1, 4000):
            with self.subTest(n=n):
                self.assertEqual(to_roman(from_roman(to_roman(n))), to_roman(n))


if __name__ == "__main__":
    unittest.main()
