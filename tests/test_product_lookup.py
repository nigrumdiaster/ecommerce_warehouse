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


@pytest.mark.django_db
def test_search_and_category_use_hash_tables_without_database_queries(
    lookup_service, django_assert_num_queries
):
    phones = Category.objects.create(name="Điện thoại")
    laptops = Category.objects.create(name="Laptop")
    phone = Product.objects.create(
        name="iPhone 15 Pro", sku="IP15P-128", category=phones,
        description="Titan tự nhiên", price=25000000
    )
    Product.objects.create(name="iPhone Laptop", sku="LAPTOP-1", category=laptops, price=20000000)
    lookup_service.load_products()

    with django_assert_num_queries(0):
        exact_sku = lookup_service.search("IP15P-128", phones.id)
        partial_name = lookup_service.search("phone 15", phones.id)
        description = lookup_service.search("titan", phones.id)
        short_query = lookup_service.search("iP", phones.id)
        wrong_category = lookup_service.search("IP15P-128", laptops.id)
        category_only = lookup_service.search(category_id=phones.id)

    assert exact_sku == [phone]
    assert partial_name == [phone]
    assert description == [phone]
    assert short_query == [phone]
    assert wrong_category == []
    assert category_only == [phone]


@pytest.mark.django_db
def test_product_list_keeps_search_and_sort_but_removes_status_filter(client, lookup_service):
    category = Category.objects.create(name="Điện thoại")
    expensive = Product.objects.create(
        name="iPhone Pro", sku="PHONE-PRO", category=category,
        price=200, is_active=False
    )
    cheap = Product.objects.create(
        name="iPhone Base", sku="PHONE-BASE", category=category, price=100
    )
    response = client.get('/product/', {
        'q': 'iPhone', 'category': str(category.id), 'status': 'active', 'sort': 'price'
    })

    assert response.status_code == 200
    assert response.context['products'] == [cheap, expensive]
    assert response.context['total_count'] == 2
    assert response.context['selected_sort'] == 'price'
    assert 'name="q"' in response.content.decode()
    assert 'name="sort"' in response.content.decode()
    assert 'name="status"' not in response.content.decode()


@pytest.mark.django_db
def test_category_hash_index_refreshes_when_product_moves_or_category_is_deleted(lookup_service):
    original = Category.objects.create(name="Điện thoại")
    destination = Category.objects.create(name="Laptop")
    destination_id = destination.id
    product = Product.objects.create(name="iPhone", sku="PHONE-1", category=original, price=100)
    assert lookup_service.search(category_id=original.id) == [product]

    product.category = destination
    product.name = "MacBook"
    product.save()
    assert lookup_service.search('iPhone', original.id) == []
    assert lookup_service.search('MacBook', destination_id) == [product]

    destination.delete()
    assert lookup_service.search(category_id=destination_id) == []
    assert lookup_service.search('MacBook')[0].category_id is None
