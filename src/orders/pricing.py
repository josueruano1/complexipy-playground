"""Order pricing rules for the playground repository."""


def process_orders(orders, rules, region, currency, fallback_rate):
    """Apply regional rules, item discounts and currency conversion."""
    total = 0.0
    rejected = []

    for order in orders:
        if order.get("status") == "paid":
            for item in order.get("items", []):
                if item["qty"] > 0:
                    if item["price"] > 100:
                        total += item["price"] * item["qty"] * 0.9
                    elif item["price"] > 50:
                        total += item["price"] * item["qty"] * 0.95
                    else:
                        total += item["price"] * item["qty"]

                    for rule in rules:
                        if rule["region"] == region:
                            if rule["kind"] == "tax":
                                total *= 1 + rule["rate"]
                            elif rule["kind"] == "discount":
                                if total > rule.get("minimum", 0):
                                    total -= rule["amount"]
                                else:
                                    rejected.append((order["id"], rule["kind"]))
                            elif rule["kind"] == "surcharge":
                                total += rule["amount"]
                else:
                    rejected.append((order["id"], "empty-line"))
        elif order.get("status") == "pending":
            if region == "eu":
                if order.get("reserved"):
                    total += 0.0
                else:
                    rejected.append((order["id"], "not_reserved"))
            else:
                rejected.append((order["id"], "pending-outside-eu"))
        else:
            rejected.append((order["id"], order.get("status", "unknown")))

    if currency != "eur":
        if fallback_rate:
            total *= fallback_rate
        else:
            raise ValueError("no conversion rate available")

    return round(total, 2), rejected


def summarise_rejections(rejected, known_reasons, limits):
    """Group rejection reasons; unknown ones fold into `other`."""
    summary = {}
    for order_id, reason in rejected:
        if reason in known_reasons:
            current = summary.setdefault(reason, [])
            bucket = reason if len(current) < limits.get(reason, 100) else "overflow"
            summary.setdefault(bucket, []).append(order_id)
        else:
            if "other" not in summary:
                summary["other"] = []
            if order_id not in summary["other"]:
                summary["other"].append(order_id)
    return summary


def order_total(items):
    """A small helper that must stay under the threshold."""
    total = 0
    for item in items:
        total += item["price"] * item["qty"]
    return total
