"""Informe mensual de ventas y cobros."""


def build_monthly_report(orders: list[dict], invoices: list[dict], period: str) -> dict:
    """Resume un mes de pedidos y facturas en un único informe."""
    report: dict = {"period": period, "revenue": 0.0, "pending": 0.0, "by_region": {}, "alerts": []}

    for order in orders:
        if order.get("period") != period:
            continue
        region = order.get("region") or "sin-region"
        if order.get("status") == "paid":
            for item in order.get("items", []):
                if item.get("quantity", 0) <= 0:
                    report["alerts"].append(f"{order['id']}: línea vacía")
                    continue
                amount = item.get("price", 0.0) * item["quantity"]
                if item.get("gift"):
                    amount = 0.0
                report["revenue"] += amount
                report["by_region"][region] = report["by_region"].get(region, 0.0) + amount
        elif order.get("status") == "pending":
            report["pending"] += order.get("total", 0.0)
        else:
            report["alerts"].append(f"{order['id']}: estado {order.get('status')}")

    for invoice in invoices:
        if invoice.get("period") == period and invoice.get("overdue"):
            if invoice.get("disputed") or invoice.get("total", 0) > 10000:
                report["alerts"].append(f"{invoice['id']}: revisar cobro")

    return report


def format_amount(amount: float, currency: str = "EUR") -> str:
    return f"{amount:,.2f} {currency}"
