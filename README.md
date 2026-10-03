# E-Commerce Warehouse Management System

<p align="center">
  <img src="https://www.djangoproject.com/m/img/logos/django-logo-negative.png" alt="Django Logo" width="200">
</p>

---

## 🛠 Yêu cầu hệ thống (Prerequisites)

- **Python** (Phiên bản 3.14)
- **pip** (Trình quản lý gói của Python)

---

## 🚀 Hướng dẫn cài đặt và khởi chạy (Installation & Setup)

### 1. Tạo và kích hoạt môi trường ảo (Virtual Environment)

- **Trên Windows (Command Prompt / PowerShell):**

  ```bash
  # Tạo môi trường ảo (tên thư mục là env)
  python -m venv env

  # Kích hoạt môi trường ảo
  # Dành cho Command Prompt:
  env\Scripts\activate.bat
  # Dành cho PowerShell:
  env\Scripts\Activate.ps1
  ```

- **Trên macOS / Linux:**

  ```bash
  # Tạo môi trường ảo
  python3 -m venv env

  # Kích hoạt môi trường ảo
  source env/bin/activate
  ```

---

### 2. Cài đặt các thư viện cần thiết (Dependencies)

Sau khi môi trường ảo đã được kích hoạt `(env)`:

```bash
pip install -r requirements.txt
```

---

### 3. Cấu hình cơ sở dữ liệu (Database Migration)

```bash
# Tạo các file migration (nếu có thay đổi models)
python manage.py makemigrations

# Thực thi migration vào cơ sở dữ liệu
python manage.py migrate
```

*(Tùy chọn)* Tạo tài khoản quản trị viên (Admin Superuser):

```bash
python manage.py createsuperuser
```

---

### 4. Chạy máy chủ phát triển (Run Development Server)

```bash
python manage.py runserver
```

Truy cập ứng dụng trên trình duyệt web:

- Trang chủ: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) hoặc [http://localhost:8000/](http://localhost:8000/)
- Trang quản trị: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

### 5. Kiểm thử thực nghiệm hiệu năng thuật toán (Run Benchmark MC1 & MC2)

Chạy kiểm thử so sánh hiệu năng giữa cấu trúc dữ liệu tối ưu (**HashTable**, **MaxHeap**) và cách tiếp cận tuyến tính (**Linear Search**, **Unsorted List**):

- **Chạy mặc định (ở các mốc quy mô 1.000, 10.000, 100.000 bản ghi):**

  ```bash
  python manage.py benchmark_mc1_mc2 --scales 1000,10000,100000
  ```

> Kết quả đo đạc sẽ được hiển thị trực tiếp trên console và tự động lưu/xuất ra file Excel `benchmark_results.xlsx` gồm 2 sheet: `MC1_Product_Lookup` và `MC2_Order_Queue`.

---

## ⏹️ Tắt máy chủ và hủy kích hoạt môi trường ảo

- Để dừng server Django: nhấn `Ctrl + C`
- Để tắt môi trường ảo:

  ```bash
  deactivate
  ```
