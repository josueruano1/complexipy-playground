"""Devoluciones de pedidos entregados."""


def _line_refund(item: dict, line: dict, policy: dict) -> float:
    """Reembolso de una línea aceptada, descontando la reposición si se abrió."""
    refund = item.get("price", 0.0) * min(line.get("quantity", 0), item.get("quantity", 0))
    if not line.get("opened"):
        return refund
    if policy.get("restocking_fee"):
        return refund - refund * policy["restocking_fee"]
    if item.get("category") == "electronics":
        return refund - refund * 0.15
    return refund


def _refund_method(order: dict, policy: dict) -> str:
    if order.get("paid_with") == "gift_card" or policy.get("store_credit_only"):
        return "store_credit"
    return "original"


def process_return(order: dict, request: dict, policy: dict) -> dict:
    """Decide si se acepta una devolución y cuánto se reembolsa."""
    result: dict = {"order": order.get("id"), "accepted": [], "rejected": [], "refund": 0.0}

    if order.get("status") != "delivered":
        result["rejected"].append("pedido no entregado")
        return result

    days = request.get("days_since_delivery", 0)
    for line in request.get("lines", []):
        item = next((i for i in order.get("items", []) if i.get("sku") == line.get("sku")), None)
        if item is None:
            result["rejected"].append(f"{line.get('sku')}: no está en el pedido")
            continue
        if days > policy.get("window_days", 30):
            if item.get("defective"):
                if days > policy.get("warranty_days", 365):
                    result["rejected"].append(f"{line.get('sku')}: garantía vencida")
                    continue
            else:
                result["rejected"].append(f"{line.get('sku')}: fuera de plazo")
                continue
        if item.get("final_sale") and not item.get("defective"):
            result["rejected"].append(f"{line.get('sku')}: venta final")
            continue
        result["accepted"].append(line.get("sku"))
        result["refund"] += _line_refund(item, line, policy)

    result["refund_method"] = _refund_method(order, policy)
    result["refund"] = round(result["refund"], 2)
    return result
