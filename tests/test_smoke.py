from src.orders.validation import validate_order
from src.utils.text import slugify


def test_slugify():
    assert slugify("Hola Mundo") == "hola-mundo"


def test_validate_order_reports_missing_items():
    assert "el pedido no tiene líneas" in validate_order({"id": "1", "customer_id": "c", "items": []})
