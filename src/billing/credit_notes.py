"""Notas de crédito sobre facturas emitidas."""


def _returned_quantity(line: dict, original: dict, reason: str) -> int:
    """Lo que se puede abonar de una línea: nunca más de lo facturado."""
    quantity = line.get("quantity", 0)
    billed = original.get("quantity", 0)
    if quantity <= billed:
        return quantity
    if reason == "damaged":
        return billed
    raise ValueError(f"{line.get('sku')}: devuelve más de lo facturado")


def _credit_line(line: dict, original: dict, reason: str) -> dict | None:
    quantity = _returned_quantity(line, original, reason)
    if quantity <= 0:
        return None
    amount = original.get("price", 0.0) * quantity * (1 - original.get("discount", 0.0))
    return {"sku": line.get("sku"), "quantity": quantity, "amount": round(amount, 2)}


def issue_credit_note(invoice: dict, lines: list[dict], reason: str) -> dict:
    """Emite una nota de crédito por las líneas devueltas de una factura."""
    if invoice.get("status") in ("void", "draft"):
        raise ValueError("la factura no admite notas de crédito")

    originals = {l.get("sku"): l for l in invoice.get("lines", [])}
    credited = []
    for line in lines:
        original = originals.get(line.get("sku"))
        credit = _credit_line(line, original, reason) if original else None
        if credit:
            credited.append(credit)

    total = round(sum(line["amount"] for line in credited), 2)
    if total > invoice.get("total", 0) or not credited:
        raise ValueError("nota de crédito inválida")
    return {"invoice": invoice.get("id"), "reason": reason, "lines": credited, "total": total}
