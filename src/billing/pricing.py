"""Aritmética de precios. Cada función hace una sola cosa."""

from decimal import Decimal


def apply_rate(amount: Decimal, rate: Decimal) -> Decimal:
    return amount * (Decimal(1) + rate)


def subtotal(unit_price: Decimal, quantity: int) -> Decimal:
    return unit_price * Decimal(quantity)


def round_money(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"))


def percentage_off(amount: Decimal, percent: int) -> Decimal:
    if percent <= 0:
        return amount
    return amount - (amount * Decimal(percent) / Decimal(100))
