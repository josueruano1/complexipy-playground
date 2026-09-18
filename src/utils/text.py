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


def capitalize_words(value: str, keep: tuple[str, ...] = ("de", "del", "la", "y")) -> str:
    """Pone en mayúscula la primera letra de cada palabra, salvo las conectoras."""
    words = []
    for index, word in enumerate(value.split()):
        if not word:
            continue
        if index > 0 and word.lower() in keep:
            words.append(word.lower())
        elif word.isupper() and len(word) > 1:
            words.append(word)
        else:
            if "-" in word:
                parts = []
                for part in word.split("-"):
                    if part:
                        parts.append(part[:1].upper() + part[1:].lower())
                    else:
                        parts.append(part)
                words.append("-".join(parts))
            else:
                words.append(word[:1].upper() + word[1:].lower())
    return " ".join(words)
