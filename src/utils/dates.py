"""Fechas de corte y periodos de facturación."""


def billing_period(day: int, month: int, year: int, cutoff: int = 25) -> str:
    """Periodo al que pertenece una fecha según el día de corte."""
    if not 1 <= month <= 12 or day < 1:
        raise ValueError("fecha inválida")
    if day > cutoff:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
    elif day > 28 and month == 2:
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            day = min(day, 29)
        else:
            if day > 29:
                raise ValueError("febrero no tiene tantos días")
            day = 28
    return f"{year}-{month:02d}"
