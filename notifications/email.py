"""Plantillas de correo para avisos de cobro."""


def render_payment_reminder(invoice: dict, customer: dict, step: str) -> dict:
    """Arma asunto y cuerpo del recordatorio que toca enviar."""
    name = customer.get("name") or "cliente"
    lang = customer.get("language", "es")
    if step == "none":
        return {}

    if step == "courtesy":
        subject = "Tu factura vence pronto" if lang == "es" else "Your invoice is due soon"
    elif step in ("first-reminder", "second-reminder"):
        subject = "Factura pendiente de pago" if lang == "es" else "Invoice overdue"
        if invoice.get("total", 0) > 1000 and step == "second-reminder":
            subject += " (importe elevado)"
    elif step == "final-notice":
        subject = "Último aviso" if lang == "es" else "Final notice"
    else:
        subject = step

    lines = [f"Hola {name},", f"La factura {invoice.get('id')} tiene un saldo de {invoice.get('total', 0)}."]
    for payment in invoice.get("payments", []):
        if payment.get("status") == "failed":
            lines.append(f"El cobro del {payment.get('date')} fue rechazado.")
    if customer.get("account_manager"):
        lines.append(f"Tu gestor es {customer['account_manager']}.")
    return {"to": customer.get("email"), "subject": subject, "body": "\n".join(lines)}
