import pytest

from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# ---------- add ----------

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-2, -3, -5),
    (-2, 5, 3),
    (0, 0, 0),
    (10**12, 10**12, 2 * 10**12),
    (2.5, 0.5, 3.0),
], ids=["positive", "negative", "mixed_signs", "zeros", "big_numbers", "floats"])
def test_add(calc, a, b, expected):
    assert calc.add(a, b) == expected


def test_add_float_precision(calc):
    # 0.1 + 0.2 = 0.30000000000000004, поэтому сравниваем приближённо
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)


# ---------- subtract ----------

@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 2),
    (3, 5, -2),
    (-5, -3, -2),
    (7, 0, 7),
    (0, 7, -7),
    (5.5, 2.25, 3.25),
])
def test_subtract(calc, a, b, expected):
    assert calc.subtract(a, b) == expected


# ---------- multiply ----------

@pytest.mark.parametrize("a, b, expected", [
    (4, 5, 20),
    (-4, 5, -20),
    (-4, -5, 20),
    (123, 0, 0),
    (1, 99, 99),
    (2.5, 4, 10.0),
])
def test_multiply(calc, a, b, expected):
    assert calc.multiply(a, b) == expected


# ---------- divide ----------

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (7, 2, 3.5),
    (-9, 3, -3),
    (-9, -3, 3),
    (0, 5, 0),
    (1, 3, pytest.approx(0.3333333)),
])
def test_divide(calc, a, b, expected):
    assert calc.divide(a, b) == expected


@pytest.mark.parametrize("a", [10, -10, 0, 2.5])
@pytest.mark.parametrize("zero", [0, 0.0])
def test_divide_by_zero_raises_exception(calc, a, zero):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль невозможно"):
        calc.divide(a, zero)


# ---------- проверка типов аргументов ----------

@pytest.mark.parametrize("method", ["add", "subtract", "multiply", "divide"])
@pytest.mark.parametrize("bad_value", ["2", None, [1], True])
def test_arithmetic_rejects_non_numbers(calc, method, bad_value):
    with pytest.raises(TypeError):
        getattr(calc, method)(bad_value, 1)


# ---------- is_prime_number ----------

@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 97, 7919])
def test_is_prime_number_true(calc, n):
    assert calc.is_prime_number(n) is True


@pytest.mark.parametrize("n", [4, 9, 15, 25, 49, 100, 7917])
def test_is_prime_number_false_for_composite(calc, n):
    assert calc.is_prime_number(n) is False


@pytest.mark.parametrize("n", [1, 0, -1, -7])
def test_is_prime_number_false_below_two(calc, n):
    assert calc.is_prime_number(n) is False


@pytest.mark.parametrize("bad_value", [7.0, "7", None, True])
def test_is_prime_number_rejects_non_integers(calc, bad_value):
    with pytest.raises(TypeError):
        calc.is_prime_number(bad_value)
