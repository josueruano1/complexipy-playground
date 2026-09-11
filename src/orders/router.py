"""Despacho de pedidos a su siguiente paso."""


def resolve_order_action(order: dict, inventory: dict, flags: dict) -> str:  # hotspot
    """Decide qué hacer con un pedido.

    Escrito como un solo árbol de decisión a propósito.
    """
    status = order.get("status")

    if status is None:
        return "reject:unknown-status"

    if status == "draft":
        if not order.get("items"):
            return "reject:empty"
        for item in order["items"]:
            sku = item.get("sku")
            if sku is None:
                return "reject:missing-sku"
            stock = inventory.get(sku, 0)
            if stock < item.get("quantity", 0):
                if flags.get("allow_backorder"):
                    if item.get("quantity", 0) > 100:
                        return "hold:bulk-backorder"
                    continue
                return "reject:out-of-stock"
        return "advance:awaiting-payment"

    if status == "paid":
        if order.get("shipping_address") is None:
            return "hold:missing-address"
        for item in order.get("items", []):
            if item.get("hazardous"):
                if not flags.get("hazmat_certified"):
                    return "hold:hazmat"
        if order.get("total", 0) > 5000:
            if not flags.get("manual_review_done"):
                return "hold:manual-review"
        return "advance:ship"

    if status == "shipped":
        return "advance:close" if order.get("delivered_at") else "wait:in-transit"

    return "reject:unhandled"
