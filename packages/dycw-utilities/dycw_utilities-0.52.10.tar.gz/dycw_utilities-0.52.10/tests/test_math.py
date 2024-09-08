from __future__ import annotations

from math import inf, nan
from re import escape
from typing import Any, ClassVar

from hypothesis import given
from hypothesis.strategies import integers
from numpy import iinfo, int8, int16, int32, int64, uint8, uint16, uint32, uint64
from pytest import approx, mark, param, raises

from utilities.math import (
    MAX_INT8,
    MAX_INT16,
    MAX_INT32,
    MAX_INT64,
    MAX_UINT8,
    MAX_UINT16,
    MAX_UINT32,
    MAX_UINT64,
    MIN_INT8,
    MIN_INT16,
    MIN_INT32,
    MIN_INT64,
    MIN_UINT8,
    MIN_UINT16,
    MIN_UINT32,
    MIN_UINT64,
    CheckIntegerError,
    NumberOfDecimalsError,
    check_integer,
    is_at_least,
    is_at_least_or_nan,
    is_at_most,
    is_at_most_or_nan,
    is_between,
    is_between_or_nan,
    is_equal,
    is_equal_or_approx,
    is_finite,
    is_finite_and_integral,
    is_finite_and_integral_or_nan,
    is_finite_and_negative,
    is_finite_and_negative_or_nan,
    is_finite_and_non_negative,
    is_finite_and_non_negative_or_nan,
    is_finite_and_non_positive,
    is_finite_and_non_positive_or_nan,
    is_finite_and_non_zero,
    is_finite_and_non_zero_or_nan,
    is_finite_and_positive,
    is_finite_and_positive_or_nan,
    is_finite_or_nan,
    is_greater_than,
    is_greater_than_or_nan,
    is_integral,
    is_integral_or_nan,
    is_less_than,
    is_less_than_or_nan,
    is_negative,
    is_negative_or_nan,
    is_non_negative,
    is_non_negative_or_nan,
    is_non_positive,
    is_non_positive_or_nan,
    is_non_zero,
    is_non_zero_or_nan,
    is_positive,
    is_positive_or_nan,
    is_zero,
    is_zero_or_finite_and_non_micro,
    is_zero_or_finite_and_non_micro_or_nan,
    is_zero_or_nan,
    is_zero_or_non_micro,
    is_zero_or_non_micro_or_nan,
    number_of_decimals,
    order_of_magnitude,
)


class TestCheckInteger:
    def test_equal_pass(self) -> None:
        check_integer(0, equal=0)

    def test_equal_fail(self) -> None:
        with raises(CheckIntegerError, match="Integer must be equal to .*; got .*"):
            check_integer(0, equal=1)

    @mark.parametrize("equal_or_approx", [param(10), param((11, 0.1))])
    def test_equal_or_approx_pass(
        self, *, equal_or_approx: int | tuple[int, float]
    ) -> None:
        check_integer(10, equal_or_approx=equal_or_approx)

    @mark.parametrize(
        ("equal_or_approx", "match"),
        [
            param(10, "Integer must be equal to .*; got .*"),
            param(
                (11, 0.1),
                r"Integer must be approximately equal to .* \(error .*\); got .*",
            ),
        ],
    )
    def test_equal_or_approx_fail(
        self, *, equal_or_approx: int | tuple[int, float], match: str
    ) -> None:
        with raises(CheckIntegerError, match=match):
            check_integer(0, equal_or_approx=equal_or_approx)

    def test_min_pass(self) -> None:
        check_integer(0, min=0)

    def test_min_error(self) -> None:
        with raises(CheckIntegerError, match="Integer must be at least .*; got .*"):
            check_integer(0, min=1)

    def test_max_pass(self) -> None:
        check_integer(0, max=1)

    def test_max_error(self) -> None:
        with raises(CheckIntegerError, match="Integer must be at most .*; got .*"):
            check_integer(1, max=0)


class TestIsAtLeast:
    @mark.parametrize(
        ("x", "y", "expected"),
        [
            param(0.0, -inf, True),
            param(0.0, -1.0, True),
            param(0.0, -1e-6, True),
            param(0.0, -1e-7, True),
            param(0.0, -1e-8, True),
            param(0.0, 0.0, True),
            param(0.0, 1e-8, True),
            param(0.0, 1e-7, False),
            param(0.0, 1e-6, False),
            param(0.0, 1.0, False),
            param(0.0, inf, False),
            param(0.0, nan, False),
        ],
    )
    def test_main(self, *, x: float, y: float, expected: bool) -> None:
        assert is_at_least(x, y, abs_tol=1e-8) is expected

    @mark.parametrize(
        "y", [param(-inf), param(-1.0), param(0.0), param(1.0), param(inf), param(nan)]
    )
    def test_nan(self, *, y: float) -> None:
        assert is_at_least_or_nan(nan, y)


class TestIsAtMost:
    @mark.parametrize(
        ("x", "y", "expected"),
        [
            param(0.0, -inf, False),
            param(0.0, -1.0, False),
            param(0.0, -1e-6, False),
            param(0.0, -1e-7, False),
            param(0.0, -1e-8, True),
            param(0.0, 0.0, True),
            param(0.0, 1e-8, True),
            param(0.0, 1e-7, True),
            param(0.0, 1e-6, True),
            param(0.0, 1.0, True),
            param(0.0, inf, True),
            param(0.0, nan, False),
        ],
    )
    def test_main(self, *, x: float, y: float, expected: bool) -> None:
        assert is_at_most(x, y, abs_tol=1e-8) is expected

    @mark.parametrize(
        "y", [param(-inf), param(-1.0), param(0.0), param(1.0), param(inf), param(nan)]
    )
    def test_nan(self, *, y: float) -> None:
        assert is_at_most_or_nan(nan, y)


class TestIsBetween:
    @mark.parametrize(
        ("x", "low", "high", "expected"),
        [
            param(0.0, -1.0, -1.0, False),
            param(0.0, -1.0, 0.0, True),
            param(0.0, -1.0, 1.0, True),
            param(0.0, 0.0, -1.0, False),
            param(0.0, 0.0, 0.0, True),
            param(0.0, 0.0, 1.0, True),
            param(0.0, 1.0, -1.0, False),
            param(0.0, 1.0, 0.0, False),
            param(0.0, 1.0, 1.0, False),
            param(nan, -1.0, 1.0, False),
        ],
    )
    def test_main(self, *, x: float, low: float, high: float, expected: bool) -> None:
        assert is_between(x, low, high, abs_tol=1e-8) is expected

    @mark.parametrize(
        "low",
        [param(-inf), param(-1.0), param(0.0), param(1.0), param(inf), param(nan)],
    )
    @mark.parametrize(
        "high",
        [param(-inf), param(-1.0), param(0.0), param(1.0), param(inf), param(nan)],
    )
    def test_nan(self, *, low: float, high: float) -> None:
        assert is_between_or_nan(nan, low, high)


class TestIsEqual:
    @mark.parametrize(
        ("x", "y", "expected"),
        [
            param(0.0, -inf, False),
            param(0.0, -1.0, False),
            param(0.0, -1e-6, False),
            param(0.0, -1e-7, False),
            param(0.0, -1e-8, False),
            param(0.0, 0.0, True),
            param(0.0, 1e-8, False),
            param(0.0, 1e-7, False),
            param(0.0, 1e-6, False),
            param(0.0, 1.0, False),
            param(0.0, inf, False),
            param(0.0, nan, False),
        ],
    )
    def test_main(self, *, x: float, y: float, expected: bool) -> None:
        assert is_equal(x, y) is expected
        assert is_equal(y, x) is expected


class TestIsEqualOrApprox:
    @mark.parametrize(
        ("x", "y", "expected"),
        [
            param(0, 0, True),
            param(0, 1, False),
            param(1, 0, False),
            param(10, (8, 0.1), False),
            param(10, (9, 0.1), True),
            param(10, (10, 0.1), True),
            param(10, (11, 0.1), True),
            param(10, (12, 0.1), False),
            param((10, 0.1), (8, 0.1), False),
            param((10, 0.1), (9, 0.1), True),
            param((10, 0.1), (10, 0.1), True),
            param((10, 0.1), (11, 0.1), True),
            param((10, 0.1), (12, 0.1), False),
        ],
    )
    def test_main(
        self, *, x: int | tuple[int, float], y: int | tuple[int, float], expected: bool
    ) -> None:
        assert is_equal_or_approx(x, y) is expected
        assert is_equal_or_approx(y, x) is expected


class TestIsFinite:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, True, True),
            param(0.0, True, True),
            param(1.0, True, True),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_finite(x) is expected
        assert is_finite_or_nan(x) is expected_nan


class TestIsFiniteAndIntegral:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-2.0, True, True),
            param(-1.5, False, False),
            param(-1.0, True, True),
            param(-0.5, False, False),
            param(-1e-6, False, False),
            param(-1e-7, False, False),
            param(-1e-8, True, True),
            param(0.0, True, True),
            param(1e-8, True, True),
            param(1e-7, False, False),
            param(1e-6, False, False),
            param(0.5, False, False),
            param(1.0, True, True),
            param(1.5, False, False),
            param(2.0, True, True),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_finite_and_integral(x, abs_tol=1e-8) is expected
        assert is_finite_and_integral_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsFiniteAndNegative:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, True, True),
            param(-1e-6, True, True),
            param(-1e-7, True, True),
            param(-1e-8, False, False),
            param(0.0, False, False),
            param(1e-8, False, False),
            param(1e-7, False, False),
            param(1e-6, False, False),
            param(1.0, False, False),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_finite_and_negative(x, abs_tol=1e-8) is expected
        assert is_finite_and_negative_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsFiniteAndNonNegative:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, False, False),
            param(-1e-6, False, False),
            param(-1e-7, False, False),
            param(-1e-8, True, True),
            param(0.0, True, True),
            param(1e-8, True, True),
            param(1e-7, True, True),
            param(1e-6, True, True),
            param(1.0, True, True),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_finite_and_non_negative(x, abs_tol=1e-8) is expected
        assert is_finite_and_non_negative_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsFiniteAndNonPositive:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, True, True),
            param(-1e-6, True, True),
            param(-1e-7, True, True),
            param(-1e-8, True, True),
            param(0.0, True, True),
            param(1e-8, True, True),
            param(1e-7, False, False),
            param(1e-6, False, False),
            param(1.0, False, False),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_finite_and_non_positive(x, abs_tol=1e-8) is expected
        assert is_finite_and_non_positive_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsFiniteAndNonZero:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, True, True),
            param(-1e-6, True, True),
            param(-1e-7, True, True),
            param(-1e-8, False, False),
            param(0.0, False, False),
            param(1e-8, False, False),
            param(1e-7, True, True),
            param(1e-6, True, True),
            param(1.0, True, True),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_finite_and_non_zero(x, abs_tol=1e-8) is expected
        assert is_finite_and_non_zero_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsFiniteAndPositive:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, False, False),
            param(-1e-6, False, False),
            param(-1e-7, False, False),
            param(-1e-8, False, False),
            param(0.0, False, False),
            param(1e-8, False, False),
            param(1e-7, True, True),
            param(1e-6, True, True),
            param(1.0, True, True),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_finite_and_positive(x, abs_tol=1e-8) is expected
        assert is_finite_and_positive_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsGreaterThan:
    @mark.parametrize(
        ("x", "y", "expected"),
        [
            param(0.0, -inf, True),
            param(0.0, -1.0, True),
            param(0.0, -1e-6, True),
            param(0.0, -1e-7, True),
            param(0.0, -1e-8, False),
            param(0.0, 0.0, False),
            param(0.0, 1e-8, False),
            param(0.0, 1e-7, False),
            param(0.0, 1e-6, False),
            param(0.0, 1.0, False),
            param(0.0, inf, False),
            param(0.0, nan, False),
        ],
    )
    def test_main(self, *, x: float, y: float, expected: bool) -> None:
        assert is_greater_than(x, y, abs_tol=1e-8) is expected

    @mark.parametrize(
        "y", [param(-inf), param(-1.0), param(0.0), param(1.0), param(inf), param(nan)]
    )
    def test_nan(self, *, y: float) -> None:
        assert is_greater_than_or_nan(nan, y)


class TestIsIntegral:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, True, True),
            param(-2.0, True, True),
            param(-1.5, False, False),
            param(-1.0, True, True),
            param(-0.5, False, False),
            param(-1e-6, False, False),
            param(-1e-7, False, False),
            param(-1e-8, True, True),
            param(0.0, True, True),
            param(1e-8, True, True),
            param(1e-7, False, False),
            param(1e-6, False, False),
            param(0.5, False, False),
            param(1.0, True, True),
            param(1.5, False, False),
            param(2.0, True, True),
            param(inf, True, True),
            param(nan, False, True),
        ],
    )
    def test_is_integral(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_integral(x, abs_tol=1e-8) is expected
        assert is_integral_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsLessThan:
    @mark.parametrize(
        ("x", "y", "expected"),
        [
            param(0.0, -inf, False),
            param(0.0, -1.0, False),
            param(0.0, -1e-6, False),
            param(0.0, -1e-7, False),
            param(0.0, -1e-8, False),
            param(0.0, 0.0, False),
            param(0.0, 1e-8, False),
            param(0.0, 1e-7, True),
            param(0.0, 1e-6, True),
            param(0.0, 1.0, True),
            param(0.0, inf, True),
            param(0.0, nan, False),
        ],
    )
    def test_main(self, *, x: float, y: float, expected: bool) -> None:
        assert is_less_than(x, y, abs_tol=1e-8) is expected

    @mark.parametrize(
        "y", [param(-inf), param(-1.0), param(0.0), param(1.0), param(inf), param(nan)]
    )
    def test_nan(self, *, y: float) -> None:
        assert is_less_than_or_nan(nan, y)


class TestIsNegative:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, True, True),
            param(-1.0, True, True),
            param(-1e-6, True, True),
            param(-1e-7, True, True),
            param(-1e-8, False, False),
            param(0.0, False, False),
            param(1e-8, False, False),
            param(1e-7, False, False),
            param(1e-6, False, False),
            param(1.0, False, False),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_negative(x, abs_tol=1e-8) is expected
        assert is_negative_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsNonNegative:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, False, False),
            param(-1e-6, False, False),
            param(-1e-7, False, False),
            param(-1e-8, True, True),
            param(0.0, True, True),
            param(1e-8, True, True),
            param(1e-7, True, True),
            param(1e-6, True, True),
            param(1.0, True, True),
            param(inf, True, True),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_non_negative(x, abs_tol=1e-8) is expected
        assert is_non_negative_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsNonPositive:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, True, True),
            param(-1.0, True, True),
            param(-1e-6, True, True),
            param(-1e-7, True, True),
            param(-1e-8, True, True),
            param(0.0, True, True),
            param(1e-8, True, True),
            param(1e-7, False, False),
            param(1e-6, False, False),
            param(1.0, False, False),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_non_positive(x, abs_tol=1e-8) is expected
        assert is_non_positive_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsNonZero:
    @mark.parametrize(
        ("x", "expected"),
        [
            param(-inf, True),
            param(-1.0, True),
            param(-1e-6, True),
            param(-1e-7, True),
            param(-1e-8, False),
            param(0.0, False),
            param(1e-8, False),
            param(1e-7, True),
            param(1e-6, True),
            param(1.0, True),
            param(inf, True),
            param(nan, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool) -> None:
        assert is_non_zero(x, abs_tol=1e-8) is expected
        assert is_non_zero_or_nan(x, abs_tol=1e-8) is expected


class TestIsPositive:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, False, False),
            param(-1e-6, False, False),
            param(-1e-7, False, False),
            param(-1e-8, False, False),
            param(0.0, False, False),
            param(1e-8, False, False),
            param(1e-7, True, True),
            param(1e-6, True, True),
            param(1.0, True, True),
            param(inf, True, True),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_positive(x, abs_tol=1e-8) is expected
        assert is_positive_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsZero:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, False, False),
            param(-1e-6, False, False),
            param(-1e-7, False, False),
            param(-1e-8, True, True),
            param(0.0, True, True),
            param(1e-8, True, True),
            param(1e-7, False, False),
            param(1e-6, False, False),
            param(1.0, False, False),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_zero(x, abs_tol=1e-8) is expected
        assert is_zero_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsZeroOrFiniteAndNonMicro:
    @mark.parametrize(
        ("x", "expected", "expected_nan"),
        [
            param(-inf, False, False),
            param(-1.0, True, True),
            param(-1e-6, True, True),
            param(-1e-7, True, True),
            param(-1e-8, False, False),
            param(0.0, True, True),
            param(1e-8, False, False),
            param(1e-7, True, True),
            param(1e-6, True, True),
            param(1.0, True, True),
            param(inf, False, False),
            param(nan, False, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool, expected_nan: bool) -> None:
        assert is_zero_or_finite_and_non_micro(x, abs_tol=1e-8) is expected
        assert is_zero_or_finite_and_non_micro_or_nan(x, abs_tol=1e-8) is expected_nan


class TestIsZeroOrNonMicro:
    @mark.parametrize(
        ("x", "expected"),
        [
            param(-inf, True),
            param(-1.0, True),
            param(-1e-6, True),
            param(-1e-7, True),
            param(-1e-8, False),
            param(0.0, True),
            param(1e-8, False),
            param(1e-7, True),
            param(1e-6, True),
            param(1.0, True),
            param(inf, True),
            param(nan, True),
        ],
    )
    def test_main(self, *, x: float, expected: bool) -> None:
        assert is_zero_or_non_micro(x, abs_tol=1e-8) is expected
        assert is_zero_or_non_micro_or_nan(x, abs_tol=1e-8) is expected


class TestMaxLongAndDouble:
    @mark.parametrize(
        ("min_value", "max_value", "dtype"),
        [
            param(MIN_INT8, MAX_INT8, int8),
            param(MIN_INT16, MAX_INT16, int16),
            param(MIN_INT32, MAX_INT32, int32),
            param(MIN_INT64, MAX_INT64, int64),
            param(MIN_UINT8, MAX_UINT8, uint8),
            param(MIN_UINT16, MAX_UINT16, uint16),
            param(MIN_UINT32, MAX_UINT32, uint32),
            param(MIN_UINT64, MAX_UINT64, uint64),
        ],
    )
    def test_main(self, *, min_value: int, max_value: int, dtype: Any) -> None:
        info = iinfo(dtype)
        assert info.min == min_value
        assert info.max == max_value


class TestNumberOfDecimals:
    max_int: ClassVar[int] = int(1e6)

    @given(integer=integers(-max_int, max_int))
    @mark.parametrize(
        ("frac", "expected"),
        [
            param(0.0, 0),
            param(0.1, 1),
            param(0.12, 2),
            param(0.123, 3),
            param(0.1234, 4),
            param(0.12345, 5),
            param(0.123456, 6),
            param(0.1234567, 7),
            param(0.12345678, 8),
            param(0.123456789, 9),
        ],
    )
    def test_main(self, *, integer: int, frac: float, expected: int) -> None:
        x = integer + frac
        result = number_of_decimals(x)
        assert result == expected

    def test_equal_fail(self) -> None:
        x = 1.401298464324817e-45
        with raises(
            NumberOfDecimalsError,
            match=escape(
                "Could not determine number of decimals of 1.401298464324817e-45 (up to 20)"
            ),
        ):
            _ = number_of_decimals(x)


class TestOrderOfMagnitude:
    @mark.parametrize(
        ("x", "exp_float", "exp_int"),
        [
            param(0.25, -0.60206, -1),
            param(0.5, -0.30103, 0),
            param(0.75, -0.1249387, 0),
            param(1.0, 0.0, 0),
            param(5.0, 0.69897, 1),
            param(10.0, 1.0, 1),
            param(50.0, 1.69897, 2),
            param(100.0, 2.0, 2),
        ],
    )
    @mark.parametrize("sign", [param(1.0), param(-1.0)])
    def test_main(
        self, *, sign: float, x: float, exp_float: float, exp_int: int
    ) -> None:
        x_use = sign * x
        res_float = order_of_magnitude(x_use)
        assert res_float == approx(exp_float)
        res_int = order_of_magnitude(x_use, round_=True)
        assert res_int == exp_int
