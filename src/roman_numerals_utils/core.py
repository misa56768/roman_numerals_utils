"""Core conversion logic for Roman numerals.

Scope decisions (stated so the tests match the code):

* Range is 1..3999.  The classical subtractive notation used here has no
  standard representation for zero or for 4000 and above (a vinculum / bar
  convention exists but is not universal).  We reject those rather than
  inventing notation.

* Input numerals for ``from_roman`` must be upper-case ASCII and use only
  the characters I, V, X, L, C, D, M.  Lower-case is rejected rather than
  silently normalized, because accepting lower-case invites subtle bugs
  when callers copy-paste from mixed-case sources and expect round-tripping
  to work.  One clear rule is easier to reason about than a tolerant parser.

* ``from_roman`` validates that the input is a *canonical* numeral -- i.e.
  the exact string that ``to_roman`` would produce for the same value.  This
  means numerals like ``IIII`` (instead of ``IV``) or ``VV`` are rejected.
  This is the strictest reasonable interpretation and it guarantees that
  ``from_roman(to_roman(n)) == n`` and ``to_roman(from_roman(s)) == s``
  for all in-range values, which is the property the library exists to
  provide.
"""

from __future__ import annotations

# Ordered largest-first.  Each tuple is (value, symbol).  The subtractive
# pairs (4, 9, 40, 90, 400, 900) are included so that ``to_roman`` can use a
# single greedy pass and still produce canonical output.
_VALUE_TABLE: tuple[tuple[int, str], ...] = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

# Reverse lookup: symbol -> value, for single-character parsing.
_SYMBOL_VALUE: dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


class RomanError(ValueError):
    """Raised when input to ``to_roman`` or ``from_roman`` is invalid.

    Subclassing ``ValueError`` lets callers catch either the specific error
    or the broader category, which is the common Python idiom for input
    validation failures.
    """


def to_roman(value: int) -> str:
    """Convert an integer to its canonical Roman numeral representation.

    Args:
        value: An integer in the range 1..3999 inclusive.

    Returns:
        The upper-case ASCII Roman numeral string.

    Raises:
        RomanError: If ``value`` is not an ``int`` or is outside 1..3999.

    Examples:
        >>> to_roman(1)
        'I'
        >>> to_roman(4)
        'IV'
        >>> to_roman(3999)
        'MMMCMXCIX'
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise RomanError(
            f"to_roman requires an int, got {type(value).__name__}"
        )
    if value < 1 or value > 3999:
        raise RomanError(
            f"to_roman value must be in 1..3999, got {value}"
        )

    remaining = value
    parts: list[str] = []
    for num, symbol in _VALUE_TABLE:
        count, remaining = divmod(remaining, num)
        if count:
            parts.append(symbol * count)
    return "".join(parts)


def from_roman(roman: str) -> int:
    """Convert a Roman numeral string to its integer value.

    The input must be a *canonical* numeral -- the exact string that
    ``to_roman`` would produce.  Non-canonical but historically attested
    forms such as ``IIII`` are rejected, as are lower-case strings and
    strings containing invalid characters.

    Args:
        roman: A canonical upper-case Roman numeral string.

    Returns:
        The integer value (1..3999).

    Raises:
        RomanError: If the input is not a string, contains invalid
            characters, is empty, is non-canonical, or represents a value
            outside 1..3999.

    Examples:
        >>> from_roman("I")
        1
        >>> from_roman("IV")
        4
        >>> from_roman("MMMCMXCIX")
        3999
    """
    if not isinstance(roman, str):
        raise RomanError(
            f"from_roman requires a str, got {type(roman).__name__}"
        )

    stripped = roman.strip()
    if not stripped:
        raise RomanError("from_roman received an empty or blank string")

    if stripped != roman:
        raise RomanError(
            "from_roman input must not have leading or trailing whitespace"
        )

    # Reject any character outside the allowed set, including lower-case.
    for ch in roman:
        if ch not in _SYMBOL_VALUE:
            raise RomanError(
                f"from_roman input contains invalid character: {ch!r}"
            )

    # Compute the integer value using the standard subtractive rule:
    # if a symbol is smaller than the symbol to its right, subtract it;
    # otherwise add it.  This correctly parses any well-formed numeral,
    # canonical or not.  We then check canonicity separately below.
    total = 0
    prev = 0
    for ch in reversed(roman):
        current = _SYMBOL_VALUE[ch]
        if current < prev:
            total -= current
        else:
            total += current
        prev = current

    if total < 1 or total > 3999:
        raise RomanError(
            f"from_roman value out of range (1..3999): got {total}"
        )

    # Canonical check: re-encoding the computed value must reproduce the
    # input exactly.  This rejects forms like IIII, VV, IC, etc.
    if to_roman(total) != roman:
        raise RomanError(
            f"from_roman input is not a canonical numeral: {roman!r}"
        )

    return total
