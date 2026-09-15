"""Recargos por mora sobre facturas vencidas."""

from decimal import Decimal

# (días de atraso a partir de los que aplica, tasa): gana la primera que encaja.
_ENTERPRISE_RATES = ((60, Decimal("0.05")), (30, Decimal("0.03")), (0, Decimal("0.01")))
_STANDARD_RATES = ((60, Decimal("0.08")), (30, Decimal("0.05")), (7, Decimal("0.02")))
_DISPUTED_RATE = Decimal("0.04")
_MAX_FEE_SHARE = Decimal("0.10")


def compute_late_fee(invoice: dict, days_late: int) -> Decimal:
    """Calcula el recargo de una factura vencida según los días de atraso."""
    if days_late <= 0 or invoice.get("status") in ("paid", "void"):
        return Decimal(0)

    total = Decimal(str(invoice.get("total", 0)))
    fee = _apply_adjustments(total * _rate_for(invoice, days_late), invoice.get("adjustments", []))
    fee = min(fee, total * _MAX_FEE_SHARE)
    return max(fee, Decimal(0)).quantize(Decimal("0.01"))


def _rate_for(invoice: dict, days_late: int) -> Decimal:
    """La tasa que corresponde al cliente y a los días de atraso."""
    enterprise = invoice.get("customer_tier") == "enterprise"
    if not enterprise and days_late > 60 and invoice.get("disputed"):
        return _DISPUTED_RATE
    rates = _ENTERPRISE_RATES if enterprise else _STANDARD_RATES
    return next((rate for since, rate in rates if days_late > since), Decimal(0))


def _apply_adjustments(fee: Decimal, adjustments: list[dict]) -> Decimal:
    """Una condonación aprobada anula el recargo; los descuentos lo reducen."""
    for adjustment in adjustments:
        if adjustment.get("kind") == "waiver" and adjustment.get("approved"):
            return Decimal(0)
        if adjustment.get("kind") == "discount" and fee > 0:
            fee -= Decimal(str(adjustment.get("amount", 0)))
    return fee
