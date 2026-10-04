from engine.datastructures import HashTable, LinkedList
from .models import Product, ProductViewHistory


class ProductLookupService:
    def __init__(self):
        self.hash_table = HashTable()
        self.category_index = HashTable()
        self.search_index = HashTable()
        self.all_products = []
        self.loaded = False

    def load_products(self):
        if self.loaded:
            return

        products = list(Product.objects.select_related('category').all())

        for product in products:
            self.hash_table.put(product.sku, product)
            category_products = self.category_index.get(product.category_id)
            if category_products is None:
                category_products = []
                self.category_index.put(product.category_id, category_products)
            category_products.append(product)

            # Chỉ mục chuỗi con để giữ cách tìm theo tên, SKU và mô tả.
            grams = set()
            for value in (product.name, product.sku, product.description or ''):
                value = value.casefold()
                for length in range(1, 4):
                    grams.update(value[i:i + length] for i in range(len(value) - length + 1))
            for gram in grams:
                matches = self.search_index.get(gram)
                if matches is None:
                    matches = []
                    self.search_index.put(gram, matches)
                matches.append(product)

        self.all_products = products
        self.loaded = True

    def lookup(self, sku):
        self.load_products()
        return self.hash_table.get(sku)

    def search(self, query='', category_id=None):
        self.load_products()
        if not query:
            if category_id is None:
                return self.all_products
            return self.category_index.get(category_id) or []

        exact = self.hash_table.get(query)
        if exact is not None:
            products = [exact]
        else:
            needle = query.casefold()
            candidates = self.search_index.get(needle[:3]) or []
            products = [
                product for product in candidates
                if any(needle in value.casefold() for value in (
                    product.name, product.sku, product.description or ''
                ))
            ]

        if category_id is not None:
            category_products = self.category_index.get(category_id) or []
            category_product_ids = {product.id for product in category_products}
            products = [product for product in products if product.id in category_product_ids]
        return products

    def invalidate(self):
        self.hash_table = HashTable()
        self.category_index = HashTable()
        self.search_index = HashTable()
        self.all_products = []
        self.loaded = False


class RecentlyViewedService:
    def __init__(self, capacity=9):
        self.capacity = capacity
        self.sessions = {}

    def get_user_list(self, session_key):
        if session_key not in self.sessions:
            self.sessions[session_key] = LinkedList(capacity=self.capacity)
            # Load từ DB nếu có lịch sử trước đó
            if session_key:
                try:
                    histories = ProductViewHistory.objects.filter(
                        session_key=session_key
                    ).select_related('product__category').order_by('viewed_at')[:self.capacity]
                    for h in histories:
                        self.sessions[session_key].add_recently_viewed(h.product)
                except Exception:
                    pass
        return self.sessions[session_key]

    def record_view(self, product, session_key, user=None):
        if not session_key:
            return

        ll = self.get_user_list(session_key)
        ll.add_recently_viewed(product)

        # Cập nhật thời điểm xem vào Database
        try:
            ProductViewHistory.objects.update_or_create(
                session_key=session_key,
                product=product,
                defaults={'user': user if (user and user.is_authenticated) else None}
            )
        except Exception:
            pass

    def get_recently_viewed(self, session_key):
        if not session_key:
            return []
        ll = self.get_user_list(session_key)
        return ll.to_list()


product_lookup_service = ProductLookupService()
recently_viewed_service = RecentlyViewedService(capacity=9)
