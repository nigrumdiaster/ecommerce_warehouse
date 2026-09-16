from engine.datastructures.hash_table import HashTable
from .models import Product


class ProductLookupService:
    def __init__(self):
        self.hash_table = HashTable()
        self.loaded = False

    def load_products(self):
        if self.loaded:
            return

        products = Product.objects.select_related('category').all()

        for product in products:
            self.hash_table.put(product.sku, product)

        self.loaded = True

    def lookup(self, sku):
        self.load_products()
        return self.hash_table.get(sku)


product_lookup_service = ProductLookupService()