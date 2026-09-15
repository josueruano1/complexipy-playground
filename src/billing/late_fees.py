"""Recargos por mora sobre facturas vencidas."""

from decimal import Decimal


def compute_late_fee(invoice: dict, days_late: int) -> Decimal:  # hotspot
    """Calcula el recargo de una factura vencida según los días de atraso."""
    total = Decimal(str(invoice.get("total", 0)))
    if days_late <= 0 or invoice.get("status") in ("paid", "void"):
        return Decimal(0)

    fee = Decimal(0)
    if invoice.get("customer_tier") == "enterprise":
        if days_late > 60:
            fee = total * Decimal("0.05")
        elif days_late > 30:
            fee = total * Decimal("0.03")
        else:
            fee = total * Decimal("0.01")
    else:
        if days_late > 60:
            if invoice.get("disputed"):
                fee = total * Decimal("0.04")
            else:
                fee = total * Decimal("0.08")
        elif days_late > 30:
            fee = total * Decimal("0.05")
        elif days_late > 7:
            fee = total * Decimal("0.02")

    for adjustment in invoice.get("adjustments", []):
        if adjustment.get("kind") == "waiver":
            if adjustment.get("approved"):
                fee = Decimal(0)
                break
        elif adjustment.get("kind") == "discount" and fee > 0:
            fee -= Decimal(str(adjustment.get("amount", 0)))

    if fee > total * Decimal("0.10"):
        fee = total * Decimal("0.10")
    return max(fee, Decimal(0)).quantize(Decimal("0.01"))
