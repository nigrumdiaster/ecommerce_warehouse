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


@pytest.mark.django_db
def test_view_lookup_by_exact_sku(client):
    cat = Category.objects.create(name="Điện thoại")
    p = Product.objects.create(name="iPhone 15 Pro", sku="IP15P-128", category=cat, price=25000000)

    # Đảm bảo nạp dữ liệu mới vào service
    from products.services import product_lookup_service
    product_lookup_service.loaded = False

    response = client.get('/product/', {'q': 'IP15P-128'})
    assert response.status_code == 200
    assert response.context['total_count'] == 1
    assert response.context['products'][0] == p


@pytest.mark.django_db
def test_view_search_by_name(client):
    cat = Category.objects.create(name="Laptop")
    p = Product.objects.create(name="MacBook Air M3", sku="MBA-M3", category=cat, price=28000000)

    response = client.get('/product/', {'q': 'MacBook'})
    assert response.status_code == 200
    assert response.context['total_count'] == 1
    assert p in response.context['products']