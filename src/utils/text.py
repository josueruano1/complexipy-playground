"""Pequeñas ayudas de texto. Todo aquí es deliberadamente plano."""


def slugify(value: str) -> str:
    return "-".join(value.lower().split())


def truncate(value: str, limit: int = 80) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 1] + "…"


def initials(full_name: str) -> str:
    parts = [p for p in full_name.split() if p]
    return "".join(p[0].upper() for p in parts[:2])


def pluralize(count: int, singular: str, plural: str) -> str:
    return singular if count == 1 else plural


def capitalize_words(value: str) -> str:
    return " ".join(word[:1].upper() + word[1:] for word in value.split())
