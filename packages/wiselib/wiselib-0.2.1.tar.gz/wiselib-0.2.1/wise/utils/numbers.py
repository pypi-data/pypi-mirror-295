from decimal import Decimal
from typing import Iterable

EPSILON4 = 1e-1
EPSILON5 = 1e-5
EPSILON6 = 1e-6
EPSILON7 = 1e-7
EPSILON8 = 1e-8
EPSILON9 = 1e-9
EPSILON10 = 1e-10

EPSILON = EPSILON6


def is_zero(value: float, eps: float = EPSILON) -> bool:
    return safe_abs(value) < eps


def safe_sum(col: Iterable[float]) -> float:
    return float(sum([Decimal(str(x)) for x in col], Decimal(0)))


def safe_prod(col: Iterable[float]) -> float:
    d = Decimal("1")
    for item in col:
        d *= Decimal(str(item))
    return float(d)


def safe_add(a: float, b: float) -> float:
    return float(Decimal(str(a)) + Decimal(str(b)))


def safe_sub(a: float, b: float) -> float:
    return float(Decimal(str(a)) - Decimal(str(b)))


def safe_mult(a: float, b: float) -> float:
    return float(Decimal(str(a)) * Decimal(str(b)))


def safe_div(a: float, b: float) -> float:
    return float(Decimal(str(a)) / Decimal(str(b)))


def safe_abs(a: float) -> float:
    return float(abs(Decimal(str(a))))


def safe_eq(a: float, b: float, eps: float = EPSILON) -> bool:
    return is_zero(safe_sub(a, b), eps=eps)


def safe_ne(a: float, b: float, eps: float = EPSILON) -> bool:
    return not safe_eq(a, b, eps=eps)


def safe_gt(a: float, b: float, eps: float = EPSILON) -> bool:
    return safe_sub(a, b) > eps


def safe_lt(a: float, b: float, eps: float = EPSILON) -> bool:
    return safe_sub(a, b) < -eps


def safe_gte(a: float, b: float, eps: float = EPSILON) -> bool:
    return safe_sub(a, b) >= -eps


def safe_lte(a: float, b: float, eps: float = EPSILON) -> bool:
    return safe_sub(a, b) <= eps


def safe_max(a: float, b: float) -> float:
    return float(max(Decimal(str(a)), Decimal(str(b))))


def safe_min(a: float, b: float) -> float:
    return float(min(Decimal(str(a)), Decimal(str(b))))
