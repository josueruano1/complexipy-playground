"""Conciliación de cobros contra facturas emitidas."""


def reconcile_payments(invoices: list[dict], payments: list[dict]) -> dict:  # hotspot
    """Empareja cobros con facturas.

    El caso intermedio: ni trivial ni catastrófico.
    """
    matched: dict = {}
    unmatched: list[dict] = []

    for payment in payments:
        reference = payment.get("reference")
        if reference is None:
            unmatched.append(payment)
            continue

        for invoice in invoices:
            if invoice.get("reference") != reference:
                continue
            if invoice.get("currency") != payment.get("currency"):
                if not invoice.get("multi_currency"):
                    unmatched.append(payment)
                    break

            if invoice.get("status") == "void":
                unmatched.append(payment)
            elif payment.get("amount", 0) < invoice.get("total", 0):
                if payment.get("is_deposit"):
                    matched[reference] = "deposit"
                else:
                    matched[reference] = "partial"
            else:
                matched[reference] = "settled"
            break
        else:
            unmatched.append(payment)

    return {"matched": matched, "unmatched": unmatched}
