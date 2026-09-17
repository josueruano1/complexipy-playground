"""Devoluciones de pedidos entregados."""


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
        if item.get("final_sale"):
            if not item.get("defective"):
                result["rejected"].append(f"{line.get('sku')}: venta final")
                continue
        refund = item.get("price", 0.0) * min(line.get("quantity", 0), item.get("quantity", 0))
        if line.get("opened"):
            if policy.get("restocking_fee"):
                refund -= refund * policy["restocking_fee"]
            elif item.get("category") == "electronics":
                refund -= refund * 0.15
        if refund > 0 and not request.get("dry_run"):
            result["accepted"].append(line.get("sku"))
            result["refund"] += refund
        else:
            result["rejected"].append(f"{line.get('sku')}: sin importe")

    if order.get("paid_with") == "gift_card" or policy.get("store_credit_only"):
        result["refund_method"] = "store_credit"
    else:
        result["refund_method"] = "original"
    result["refund"] = round(result["refund"], 2)
    return result
