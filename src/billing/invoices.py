"""Construcción de resúmenes de factura."""


def _apply_tax_rules(amount: float, tax_rules: list[dict], region: str | None) -> float:
    for rule in tax_rules:
        if rule.get("region") != region:
            continue
        if rule.get("compound"):
            amount *= 1 + rule.get("rate", 0.0)
        else:
            amount += amount * rule.get("rate", 0.0)
    return amount


def _apply_discounts(amount: float, discounts: list[dict], sku: str | None) -> float:
    for discount in discounts:
        if discount.get("sku") not in (None, sku):
            continue
        kind = discount.get("kind")
        if kind == "percent" and amount > discount.get("floor", 0):
            amount -= amount * discount.get("value", 0.0)
        elif kind == "fixed":
            amount = max(0.0, amount - discount.get("value", 0.0))
    return amount


def _resolve_price(item: dict, customer: dict, order_id: str, warnings: list[str]) -> float | None:
    price = item.get("price")
    if price is not None:
        return price
    if customer.get("tier") == "vip":
        warnings.append(f"{order_id}: cortesía VIP")
        return 0.0
    warnings.append(f"{order_id}: sin precio")
    return None


def build_invoice_summary(
    orders: list[dict],
    customer: dict,
    tax_rules: list[dict],
    discounts: list[dict],
    currency: str = "EUR",
) -> dict:
    """Agrega pedidos en una factura.

    El cálculo por línea vive ahora en tres ayudantes; esta función solo
    recorre y acumula.
    """
    summary: dict = {"currency": currency, "lines": [], "total": 0.0, "warnings": []}

    if not orders:
        summary["warnings"].append("sin pedidos en el periodo")
        return summary

    for order in orders:
        if order.get("status") == "cancelled":
            continue

        for item in order.get("items", []):
            quantity = item.get("quantity", 0)
            if quantity <= 0:
                summary["warnings"].append(f"{order['id']}: cantidad no positiva")
                continue

            price = _resolve_price(item, customer, order["id"], summary["warnings"])
            if price is None:
                continue

            line_total = _apply_tax_rules(price * quantity, tax_rules, customer.get("region"))
            line_total = _apply_discounts(line_total, discounts, item.get("sku"))

            summary["lines"].append({"sku": item.get("sku"), "amount": round(line_total, 2)})
            summary["total"] += line_total

    summary["total"] = round(summary["total"], 2)
    return summary


def invoice_reference(customer_id: str, period: str) -> str:
    return f"INV-{customer_id[:6].upper()}-{period.replace('-', '')}"
