from django.core.management.base import BaseCommand
from products.models import Category, Product
from inventory.models import Supplier, Stock


class Command(BaseCommand):
    help = 'Khoi tao du lieu mau cho danh muc, san pham va ton kho'

    def handle(self, *args, **options):
        self.stdout.write("Starting sample data seeding...")

        # 1. Tạo Danh Mục
        categories_data = [
            {"name": "Điện thoại & Tablet", "description": "Điện thoại thông minh, máy tính bảng và phụ kiện"},
            {"name": "Laptop & Máy tính", "description": "Laptop văn phòng, laptop gaming, PC đồng bộ"},
            {"name": "Phụ kiện công nghệ", "description": "Tai nghe, sạc cáp, bàn phím, chuột không dây"},
            {"name": "Thiết bị thông minh", "description": "Đồng hồ thông minh, camera an ninh, thiết bị Smarthome"},
            {"name": "Gia dụng thông minh", "description": "Robot hút bụi, nồi chiên, máy lọc không khí"},
        ]

        categories = {}
        for cat in categories_data:
            obj, created = Category.objects.get_or_create(
                name=cat["name"],
                defaults={"description": cat["description"]}
            )
            categories[obj.name] = obj
            if created:
                self.stdout.write(f"  + Category created: {obj.name.encode('ascii', 'replace').decode()}")

        # 2. Tạo Nhà Cung Cấp
        Supplier.objects.get_or_create(
            name="Apple Vietnam Distributor",
            defaults={"contact_email": "supply@apple.vn", "phone": "0281234567", "address": "Quận 1, TP.HCM"}
        )
        Supplier.objects.get_or_create(
            name="Samsung Electronics VN",
            defaults={"contact_email": "sales@samsung.vn", "phone": "0249876543", "address": "Bắc Ninh, VN"}
        )

        # 3. Danh sách Sản Phẩm Mẫu
        sample_products = [
            {
                "name": "iPhone 15 Pro Max 256GB - Titan Tự Nhiên",
                "sku": "IP15PM-256-NT",
                "category": categories["Điện thoại & Tablet"],
                "price": 29990000,
                "cost_price": 26500000,
                "description": "Chip A17 Pro mạnh mẽ, khung viền titan siêu bền nhẹ, hệ thống camera 5x zoom quang học đỉnh cao.",
                "is_active": True,
                "stock_quantity": 65,
            },
            {
                "name": "Samsung Galaxy S24 Ultra 512GB - Xám Titan",
                "sku": "SS-S24U-512-GR",
                "category": categories["Điện thoại & Tablet"],
                "price": 31490000,
                "cost_price": 27000000,
                "description": "Tích hợp Galaxy AI toàn diện, bút S-Pen tiện lợi, camera 200MP bắt trọn mọi chi tiết sắc nét.",
                "is_active": True,
                "stock_quantity": 45,
            },
            {
                "name": "MacBook Pro 14 M3 Pro (18GB / 512GB SSD) - Space Black",
                "sku": "MBP14-M3P-BLK",
                "category": categories["Laptop & Máy tính"],
                "price": 49990000,
                "cost_price": 44000000,
                "description": "Màn hình Liquid Retina XDR 120Hz rực rỡ, chip M3 Pro xử lý đồ họa và render video mượt mà.",
                "is_active": True,
                "stock_quantity": 25,
            },
            {
                "name": "Laptop Gaming ASUS ROG Zephyrus G16 (RTX 4070)",
                "sku": "ROG-G16-4070",
                "category": categories["Laptop & Máy tính"],
                "price": 45990000,
                "cost_price": 40500000,
                "description": "Màn hình OLED 2.5K 240Hz, card đồ họa RTX 4070 cân mọi tựa game AAA và thiết kế 3D chuyên sâu.",
                "is_active": True,
                "stock_quantity": 20,
            },
            {
                "name": "Bàn phím cơ không dây Keychron Q1 Pro (Gateron Red)",
                "sku": "KB-KEY-Q1PRO",
                "category": categories["Phụ kiện công nghệ"],
                "price": 4290000,
                "cost_price": 3400000,
                "description": "Vỏ nhôm CNC nguyên khối cao cấp, mạch xuôi hotswap, kết nối Bluetooth 5.1 và dây Type-C.",
                "is_active": True,
                "stock_quantity": 85,
            },
            {
                "name": "Chuột công thái học Logitech MX Master 3S - Graphite",
                "sku": "LOGI-MXM-3S",
                "category": categories["Phụ kiện công nghệ"],
                "price": 2490000,
                "cost_price": 1900000,
                "description": "Cuộn siêu tốc Magspeed 1000 dòng/giây, click êm ái Quiet Clicks, cảm biến 8000 DPI trên mọi bề mặt.",
                "is_active": True,
                "stock_quantity": 140,
            },
            {
                "name": "Tai nghe chống ồn Sony WH-1000XM5 - Đen",
                "sku": "SONY-WH-XM5-BK",
                "category": categories["Phụ kiện công nghệ"],
                "price": 7990000,
                "cost_price": 6500000,
                "description": "Công nghệ chống ồn chủ động ANC hàng đầu, chất âm Hi-Res Audio, thời lượng pin lên đến 30 giờ liên tục.",
                "is_active": True,
                "stock_quantity": 45,
            },
            {
                "name": "Apple Watch Ultra 2 GPS + Cellular 49mm Dây Alpine",
                "sku": "AW-ULTRA2-49",
                "category": categories["Thiết bị thông minh"],
                "price": 21490000,
                "cost_price": 18900000,
                "description": "Khung titan 49mm chuyên dụng thể thao mạo hiểm, độ sáng màn hình 3000 nits, định vị GPS kép chuẩn xác.",
                "is_active": True,
                "stock_quantity": 30,
            },
            {
                "name": "Robot hút bụi lau nhà Dreame L20 Ultra",
                "sku": "ROBOT-DREAME-L20",
                "category": categories["Gia dụng thông minh"],
                "price": 18990000,
                "cost_price": 15500000,
                "description": "Lực hút cực mạnh 7000Pa, tự động giặt sấy giẻ lau bằng nước nóng, tránh vật cản AI thông minh.",
                "is_active": True,
                "stock_quantity": 24,
            },
            {
                "name": "Củ sạc nhanh Anker GaNPrime 65W 3 cổng",
                "sku": "ANKER-GAN-65W",
                "category": categories["Phụ kiện công nghệ"],
                "price": 890000,
                "cost_price": 600000,
                "description": "Công nghệ GaN 3 tối ưu kích thước siêu nhỏ gọn, sạc đồng thời Laptop, iPad và điện thoại nhanh chóng.",
                "is_active": True,
                "stock_quantity": 220,
            },
            {
                "name": "iPad Pro 11 M4 Wi-Fi 256GB - Space Black",
                "sku": "IPAD-P11-M4-256",
                "category": categories["Điện thoại & Tablet"],
                "price": 28990000,
                "cost_price": 25200000,
                "description": "Màn hình Ultra Retina XDR OLED kép siêu mỏng 5.1mm, chip M4 đỉnh cao hiệu năng đồ họa.",
                "is_active": True,
                "stock_quantity": 35,
            },
            {
                "name": "Máy lọc không khí Xiaomi Smart Air Purifier 4 Pro",
                "sku": "MIAIR-4PRO",
                "category": categories["Gia dụng thông minh"],
                "price": 4690000,
                "cost_price": 3800000,
                "description": "Lọc sạch bụi mịn PM2.5, khử mùi hiệu quả cho phòng diện tích tới 60m2, điều khiển qua app thông minh.",
                "is_active": False,
                "stock_quantity": 5,
            }
        ]

        count = 0
        for p_data in sample_products:
            stock_qty = p_data.pop("stock_quantity")

            product, created = Product.objects.update_or_create(
                sku=p_data["sku"],
                defaults=p_data
            )

            # Cập nhật tồn kho
            Stock.objects.update_or_create(
                product=product,
                defaults={"quantity": stock_qty, "min_threshold": 5}
            )

            count += 1
            action = "Created" if created else "Updated"
            self.stdout.write(f"  + {action}: [{product.sku}]")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} products, categories, suppliers, and stocks!"))
