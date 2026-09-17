"""Recordatorios de cobro para facturas vencidas."""


def next_dunning_step(invoice: dict, history: list[dict], today: int) -> str:
    """Elige el siguiente recordatorio para una factura vencida."""
    if invoice.get("status") in ("paid", "void"):
        return "none"

    days_late = today - invoice.get("due_day", today)
    if days_late <= 0:
        return "none"

    sent = [step for step in history if step.get("invoice") == invoice.get("id")]
    last = sent[-1]["kind"] if sent else None

    if invoice.get("disputed"):
        if last == "dispute-ack":
            return "none"
        return "dispute-ack"

    if days_late > 60:
        if invoice.get("customer_tier") == "enterprise":
            if last != "account-manager":
                return "account-manager"
            return "none"
        if last == "final-notice":
            if invoice.get("total", 0) > 1000:
                return "collections"
            return "none"
        return "final-notice"

    if days_late > 30:
        if last in ("second-reminder", "final-notice"):
            return "none"
        for step in sent:
            if step.get("kind") == "promise-to-pay" and step.get("until_day", 0) >= today:
                return "none"
        return "second-reminder"

    if days_late > 7:
        if not sent or last == "courtesy":
            return "first-reminder"
        return "none"

    return "courtesy" if not sent else "none"
