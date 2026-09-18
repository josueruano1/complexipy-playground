"""Exportador antiguo, escrito para Python 2. No se usa; se conserva como referencia."""


def export_rows(rows):
    for row in rows:
        print "%s;%s" % (row["id"], row["total"])
