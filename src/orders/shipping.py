"""Coste de envío de un pedido según destino, peso y tipo de cliente."""

from decimal import Decimal


def compute_shipping_cost(order: dict) -> Decimal:
    """Calcula el coste de envío de un pedido."""
    items = order.get("items", [])
    destination = order.get("destination", {})
    customer = order.get("customer", {})
    cost = Decimal(0)

    if not items:
        return cost

    weight = Decimal(0)
    for item in items:
        if item.get("digital"):
            continue
        if item.get("weight") is not None:
            weight += Decimal(str(item["weight"])) * item.get("quantity", 1)
        else:
            if item.get("category") == "furniture":
                weight += Decimal("25") * item.get("quantity", 1)
            elif item.get("category") == "electronics":
                weight += Decimal("3") * item.get("quantity", 1)
            else:
                weight += Decimal("1") * item.get("quantity", 1)

    if weight == 0:
        return cost

    country = destination.get("country")
    if country == "ES":
        if destination.get("island"):
            cost = Decimal("12") + weight * Decimal("0.9")
        else:
            if weight > 20:
                cost = Decimal("8") + weight * Decimal("0.4")
            else:
                cost = Decimal("4.5")
    elif country in ("PT", "FR", "DE", "IT"):
        if weight > 20:
            cost = Decimal("15") + weight * Decimal("0.7")
        else:
            cost = Decimal("9")
    else:
        if destination.get("express"):
            cost = Decimal("40") + weight * Decimal("2.5")
        else:
            cost = Decimal("25") + weight * Decimal("1.5")

    if customer.get("tier") == "enterprise":
        cost = cost * Decimal("0.8")
    elif customer.get("tier") == "premium":
        if order.get("total", 0) > 100 and country == "ES":
            cost = Decimal(0)
        else:
            cost = cost * Decimal("0.9")

    for coupon in order.get("coupons", []):
        if coupon.get("kind") == "free_shipping":
            if not coupon.get("expired") and (coupon.get("country") is None or coupon.get("country") == country):
                return Decimal(0)
        elif coupon.get("kind") == "shipping_discount" and cost > 0:
            cost -= Decimal(str(coupon.get("amount", 0)))

    return max(cost, Decimal(0)).quantize(Decimal("0.01"))
