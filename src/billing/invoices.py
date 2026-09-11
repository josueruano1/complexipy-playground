"""Construcción de resúmenes de factura."""


def build_invoice_summary(  # hotspot
    orders: list[dict],
    customer: dict,
    tax_rules: list[dict],
    discounts: list[dict],
    currency: str = "EUR",
) -> dict:
    """Agrega pedidos en una factura.

    Deliberadamente monolítica: impuestos, descuentos y avisos resueltos en
    el mismo bucle. Es el peor punto del proyecto.
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

            price = item.get("price")
            if price is None:
                if customer.get("tier") == "vip":
                    price = 0.0
                    summary["warnings"].append(f"{order['id']}: cortesía VIP")
                else:
                    summary["warnings"].append(f"{order['id']}: sin precio")
                    continue

            line_total = price * quantity

            for rule in tax_rules:
                if rule.get("region") == customer.get("region"):
                    if rule.get("compound"):
                        line_total *= 1 + rule.get("rate", 0.0)
                    else:
                        line_total += line_total * rule.get("rate", 0.0)

            for discount in discounts:
                if discount.get("sku") in (None, item.get("sku")):
                    if discount.get("kind") == "percent":
                        if line_total > discount.get("floor", 0):
                            line_total -= line_total * discount.get("value", 0.0)
                    elif discount.get("kind") == "fixed":
                        line_total = max(0.0, line_total - discount.get("value", 0.0))

            summary["lines"].append({"sku": item.get("sku"), "amount": round(line_total, 2)})
            summary["total"] += line_total

    summary["total"] = round(summary["total"], 2)
    return summary


def invoice_reference(customer_id: str, period: str) -> str:
    return f"INV-{customer_id[:6].upper()}-{period.replace('-', '')}"
