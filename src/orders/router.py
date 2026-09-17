"""Despacho de pedidos a su siguiente paso."""


def _resolve_draft(order: dict, inventory: dict, flags: dict) -> str:
    """Un borrador avanza solo si cada línea tiene SKU y existencias."""
    if not order.get("items"):
        return "reject:empty"
    for item in order["items"]:
        sku = item.get("sku")
        if sku is None:
            return "reject:missing-sku"
        if inventory.get(sku, 0) >= item.get("quantity", 0):
            continue
        if not flags.get("allow_backorder"):
            return "reject:out-of-stock"
        if item.get("quantity", 0) > 100:
            return "hold:bulk-backorder"
    return "advance:awaiting-payment"


def _resolve_paid(order: dict, flags: dict) -> str:
    """Un pedido pagado se envía salvo que falte algo por revisar."""
    if order.get("shipping_address") is None:
        return "hold:missing-address"
    hazardous = any(item.get("hazardous") for item in order.get("items", []))
    if hazardous and not flags.get("hazmat_certified"):
        return "hold:hazmat"
    if order.get("total", 0) > 5000 and not flags.get("manual_review_done"):
        return "hold:manual-review"
    return "advance:ship"


def resolve_order_action(order: dict, inventory: dict, flags: dict) -> str:
    """Decide qué hacer con un pedido según su estado."""
    status = order.get("status")
    if status is None:
        return "reject:unknown-status"
    if status == "draft":
        return _resolve_draft(order, inventory, flags)
    if status == "paid":
        return _resolve_paid(order, flags)
    if status == "shipped":
        return "advance:close" if order.get("delivered_at") else "wait:in-transit"
    return "reject:unhandled"
