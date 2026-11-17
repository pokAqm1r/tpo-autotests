"""Калькулятор с бизнес-логикой для модульного тестирования."""
import math


class Calculator:

    @staticmethod
    def _check_number(*values):
        """Разрешены только int и float (bool не считается числом)."""
        for value in values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"Ожидалось число, получено: {value!r}")

    def add(self, a, b):
        self._check_number(a, b)
        return a + b

    def subtract(self, a, b):
        self._check_number(a, b)
        return a - b

    def multiply(self, a, b):
        self._check_number(a, b)
        return a * b

    def divide(self, a, b):
        self._check_number(a, b)
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b

    def is_prime_number(self, n):
        """True, если n — простое число (натуральное, больше 1)."""
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(f"Ожидалось целое число, получено: {n!r}")
        if n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        for divisor in range(3, math.isqrt(n) + 1, 2):
            if n % divisor == 0:
                return False
        return True
