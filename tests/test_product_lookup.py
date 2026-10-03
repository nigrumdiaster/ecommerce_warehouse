import pytest

from products.models import Product, Category
from products.services import (
    ProductLookupService,
    product_lookup_service,
)


@pytest.fixture
def lookup_service():
    product_lookup_service.invalidate()

    yield product_lookup_service

    product_lookup_service.invalidate()


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
def test_view_lookup_by_exact_sku(client, lookup_service):
    category = Category.objects.create(name="Điện thoại")

    product = Product.objects.create(
        name="iPhone 15 Pro",
        sku="IP15P-128",
        category=category,
        price=25000000
    )

    lookup_service.invalidate()

    response = client.get(
        "/product/",
        {"q": "IP15P-128"}
    )

    assert response.status_code == 200
    assert response.context["total_count"] == 1
    assert response.context["products"][0] == product


@pytest.mark.django_db
def test_view_search_by_name(client):
    category = Category.objects.create(name="Laptop")

    product = Product.objects.create(
        name="MacBook Air M3",
        sku="MBA-M3",
        category=category,
        price=28000000
    )

    response = client.get(
        "/product/",
        {"q": "MacBook"}
    )

    assert response.status_code == 200
    assert response.context["total_count"] == 1
    assert product in response.context["products"]


@pytest.mark.django_db
def test_product_added_after_hash_loaded(lookup_service):
    lookup_service.load_products()

    assert lookup_service.loaded is True

    product = Product.objects.create(
        name="New Product",
        sku="NEW-SKU-001",
        price=100000
    )

    assert lookup_service.loaded is False

    result = lookup_service.lookup("NEW-SKU-001")

    assert result is not None
    assert result.id == product.id


@pytest.mark.django_db
def test_product_updated_after_hash_loaded(lookup_service):
    product = Product.objects.create(
        name="Old Name",
        sku="UPDATE-SKU-001",
        price=100000
    )

    result = lookup_service.lookup("UPDATE-SKU-001")

    assert result is not None
    assert result.name == "Old Name"
    assert lookup_service.loaded is True

    product.name = "New Name"
    product.save()

    assert lookup_service.loaded is False

    result = lookup_service.lookup("UPDATE-SKU-001")

    assert result is not None
    assert result.name == "New Name"


@pytest.mark.django_db
def test_product_sku_changed_after_hash_loaded(lookup_service):
    product = Product.objects.create(
        name="Product A",
        sku="OLD-SKU",
        price=100000
    )

    result = lookup_service.lookup("OLD-SKU")

    assert result is not None
    assert result.id == product.id
    assert lookup_service.loaded is True

    product.sku = "NEW-SKU"
    product.save()

    assert lookup_service.loaded is False

    old_result = lookup_service.lookup("OLD-SKU")
    new_result = lookup_service.lookup("NEW-SKU")

    assert old_result is None
    assert new_result is not None
    assert new_result.id == product.id


@pytest.mark.django_db
def test_product_deleted_after_hash_loaded(lookup_service):
    product = Product.objects.create(
        name="Delete Product",
        sku="DELETE-SKU-001",
        price=100000
    )

    result = lookup_service.lookup("DELETE-SKU-001")

    assert result is not None
    assert result.id == product.id
    assert lookup_service.loaded is True

    product.delete()

    assert lookup_service.loaded is False

    result = lookup_service.lookup("DELETE-SKU-001")

    assert result is None


@pytest.mark.django_db
def test_lookup_after_load_uses_no_database_query(
    lookup_service,
    django_assert_num_queries
):
    category = Category.objects.create(
        name="Điện thoại test RAM"
    )

    product = Product.objects.create(
        name="iPhone Test",
        sku="RAM-SKU-001",
        category=category,
        price=20000000
    )

    lookup_service.invalidate()
    lookup_service.load_products()

    assert lookup_service.loaded is True

    with django_assert_num_queries(0):
        result = lookup_service.lookup("RAM-SKU-001")

    assert result is not None
    assert result.id == product.id