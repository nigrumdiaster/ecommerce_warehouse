class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.product_id = None
        self.product_name = None
class ProductTrie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, name, product_id):
        node = self.root
        for char in name.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.product_id = product_id
        node.product_name = name
    def autocomplete(self, prefix, limit=5):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._dfs(node, results, limit)
        return results
    def _dfs(self, node, results, limit):
        if len(results) >= limit:
            return
        if node.is_end:
            results.append({
                'id': node.product_id,
                'name': node.product_name
            })
        for char in node.children:
            self._dfs(node.children[char], results, limit)
def build_trie_from_db():
    from .models import Product
    trie = ProductTrie()
    # Lấy toàn bộ sản phẩm trong DB nạp vào cây
    try:
        products = Product.objects.all()
        for p in products:
            trie.insert(p.name, p.id)
    except Exception:
        pass  # Đề phòng trường hợp cơ sở dữ liệu chưa sẵn sàng

    return trie
trie_instance = build_trie_from_db()