# roman_numerals_utils

Convert between integers (1..3999) and canonical Roman numerals, in both
directions.

```python
from roman_numerals_utils import to_roman, from_roman, RomanError

to_roman(49)      # -> "XLIX"
from_roman("XLIX") # -> 49

try:
    from_roman("IIII")
except RomanError:
    pass  # non-canonical input is rejected
```

## Why this exists

The specific problem: needing a pair of converters that are exact inverses
of each other -- ``from_roman(to_roman(n)) == n`` and
``to_roman(from_roman(s)) == s`` -- so that values can be stored as
numerals and round-tripped losslessly.

The trade-off: to guarantee that property, ``from_roman`` only accepts
*canonical* numerals (the exact strings ``to_roman`` produces).  This
rejects historically attested but non-standard forms like ``IIII`` for 4.
If you need to parse loose, non-canonical input, this library is the wrong
choice.

## Edge cases you will hit

* **Range is 1..3999.** Zero, negatives, and 4000+ raise `RomanError`.
  There is no standard canonical representation for those values.
* **Lower-case is rejected.** Only upper-case ASCII `IVXLCDM` is accepted.
* **Whitespace is rejected.** `" IV"` raises rather than being silently
  stripped, so callers cannot accidentally accept padded input.
* **Booleans are rejected.** `to_roman(True)` raises, even though `bool`
  is a subclass of `int`, because converting `True` to `"I"` is almost
  never the caller's intent.
* **Non-canonical numerals are rejected.** `IIII`, `VV`, `IC` all raise
  `RomanError` even though they have unambiguous integer values.

## Run the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
