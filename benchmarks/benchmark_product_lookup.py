import time
from engine.datastructures.hash_table import HashTable


def create_products(n):
    products = []

    for i in range(n):
        product = {
            "sku": f"SKU-{i:08d}",
            "name": f"Product {i}"
        }
        products.append(product)

    return products


def linear_search(products, sku):
    for product in products:
        if product["sku"] == sku:
            return product

    return None


def build_hash_table(products):
    hash_table = HashTable()

    for product in products:
        hash_table.put(product["sku"], product)

    return hash_table


def benchmark_lookup(products, hash_table, target, repeat=1000):
    start = time.perf_counter()

    for _ in range(repeat):
        linear_search(products, target)

    linear_time = time.perf_counter() - start

    start = time.perf_counter()

    for _ in range(repeat):
        hash_table.get(target)

    hash_time = time.perf_counter() - start

    return linear_time, hash_time


def run_benchmark(n):
    print(f"\n===== {n:,} PRODUCTS =====")

    products = create_products(n)

    start = time.perf_counter()
    hash_table = build_hash_table(products)
    build_time = time.perf_counter() - start

    found_target = f"SKU-{n - 1:08d}"
    not_found_target = "SKU-NOT-FOUND"

    linear_found, hash_found = benchmark_lookup(
        products,
        hash_table,
        found_target
    )

    linear_not_found, hash_not_found = benchmark_lookup(
        products,
        hash_table,
        not_found_target
    )

    print(f"Build HashTable: {build_time:.6f} s")

    print("\nFOUND:")
    print(f"Linear Search: {linear_found:.6f} s")
    print(f"HashTable:     {hash_found:.6f} s")

    print("\nNOT FOUND:")
    print(f"Linear Search: {linear_not_found:.6f} s")
    print(f"HashTable:     {hash_not_found:.6f} s")


if __name__ == "__main__":
    run_benchmark(10_000)
    run_benchmark(100_000)