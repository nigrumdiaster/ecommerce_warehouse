from engine.datastructures.hash_table import HashTable
from .models import Product


class ProductLookupService:
    def __init__(self):
        self.hash_table = HashTable()

    def load_products(self):
        products = Product.objects.all()

        for product in products:
            self.hash_table.put(product.sku, product)

    def lookup(self, sku):
        return self.hash_table.get(sku)