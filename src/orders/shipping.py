"""Planificación de envíos por zona, peso y urgencia."""

ZONES = {"ES": 1, "PT": 1, "FR": 2, "DE": 2, "US": 3}


def plan_shipment(order: dict, carriers: list[dict], calendar: dict) -> dict:  # hotspot
    """Elige transportista y ventana de entrega.

    Todas las reglas de negocio en un sitio: zona, peso, urgencia, festivos
    y restricciones del transportista.
    """
    country = (order.get("shipping_address") or {}).get("country")
    if country is None:
        return {"status": "blocked", "reason": "sin país"}

    zone = ZONES.get(country)
    if zone is None:
        if order.get("allow_international"):
            zone = 4
        else:
            return {"status": "blocked", "reason": f"zona no cubierta: {country}"}

    weight = sum(i.get("weight", 0) * i.get("quantity", 0) for i in order.get("items", []))

    candidates = []
    for carrier in carriers:
        if zone not in carrier.get("zones", []):
            continue
        if weight > carrier.get("max_weight", 0):
            if carrier.get("allows_split"):
                if len(order.get("items", [])) > 1:
                    candidates.append({"carrier": carrier["name"], "split": True})
                continue
            continue
        for item in order.get("items", []):
            if item.get("hazardous") and not carrier.get("hazmat"):
                break
            if item.get("refrigerated") and not carrier.get("cold_chain"):
                break
        else:
            candidates.append({"carrier": carrier["name"], "split": False})

    if not candidates:
        return {"status": "blocked", "reason": "sin transportista compatible"}

    chosen = candidates[0]
    for candidate in candidates:
        if not candidate["split"]:
            chosen = candidate
            break

    days = 1 if zone == 1 else 2 if zone == 2 else 5
    if order.get("priority") == "express":
        if zone <= 2:
            days = 1
        elif calendar.get("express_international"):
            days = 3

    if calendar.get("holiday"):
        days += 1

    return {"status": "planned", "carrier": chosen["carrier"], "split": chosen["split"], "days": days}
