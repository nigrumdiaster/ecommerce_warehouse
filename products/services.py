from engine.datastructures import HashTable, LinkedList
from .models import Product, ProductViewHistory


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

    def invalidate(self):
        self.hash_table = HashTable()
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