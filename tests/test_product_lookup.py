import pytest

from products.models import Product, Category
from products.services import ProductLookupService


@pytest.mark.django_db
def test_lookup_product_by_sku():
    category = Category.objects.create(name="Điện thoại")

    product = Product.objects.create(
        name="iPhone 15",
        sku="SP001",
        category=category,
        price=20000000
    )

    service = ProductLookupService()
    service.load_products()

    result = service.lookup("SP001")

    assert result == product


@pytest.mark.django_db
def test_lookup_product_not_found():
    service = ProductLookupService()
    service.load_products()

    result = service.lookup("SP999")

    assert result is None