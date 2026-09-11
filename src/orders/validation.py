"""Validación de pedidos: complejidad media, por debajo del umbral."""

REQUIRED_FIELDS = ("id", "customer_id", "items")


def validate_order(order: dict) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in order:
            errors.append(f"falta el campo obligatorio: {field}")

    items = order.get("items") or []
    if not items:
        errors.append("el pedido no tiene líneas")

    for index, item in enumerate(items):
        if item.get("quantity", 0) <= 0:
            errors.append(f"línea {index}: cantidad no positiva")
        if item.get("sku") is None:
            errors.append(f"línea {index}: sin SKU")

    return errors


def is_shippable(order: dict) -> bool:
    if order.get("status") != "paid":
        return False
    return bool(order.get("shipping_address"))
