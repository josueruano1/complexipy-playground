"""Notas de crédito sobre facturas emitidas."""


def issue_credit_note(invoice: dict, lines: list[dict], reason: str) -> dict:
    """Emite una nota de crédito por las líneas devueltas de una factura."""
    note: dict = {"invoice": invoice.get("id"), "reason": reason, "lines": [], "total": 0.0}

    if invoice.get("status") in ("void", "draft"):
        raise ValueError("la factura no admite notas de crédito")

    for line in lines:
        original = next((l for l in invoice.get("lines", []) if l.get("sku") == line.get("sku")), None)
        if original is None:
            continue
        quantity = line.get("quantity", 0)
        if quantity <= 0:
            continue
        if quantity > original.get("quantity", 0):
            if reason == "damaged":
                quantity = original.get("quantity", 0)
            elif reason == "wrong-item":
                quantity = original.get("quantity", 0)
            else:
                raise ValueError(f"{line.get('sku')}: devuelve más de lo facturado")
        amount = original.get("price", 0.0) * quantity
        if original.get("discount"):
            if original.get("discount_kind") == "fixed":
                amount -= original["discount"]
            else:
                amount -= amount * original["discount"]
        note["lines"].append({"sku": line.get("sku"), "quantity": quantity, "amount": round(amount, 2)})
        note["total"] += amount

    if note["total"] > invoice.get("total", 0) or not note["lines"]:
        raise ValueError("nota de crédito inválida")
    note["total"] = round(note["total"], 2)
    return note
