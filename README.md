# ⚡ FlashSale Shopee - Website Tự Động

Website hiển thị sản phẩm FlashSale Shopee với link affiliate, tự động cập nhật từ dữ liệu thu thập.

## 🎯 Tính Năng

- ✅ Hiển thị sản phẩm FlashSale với giá ưu đãi
- ✅ Link affiliate tự động
- ✅ Filter theo Shop Mall, Rating, Deal 1K
- ✅ Search sản phẩm
- ✅ Responsive design (Mobile & Desktop)
- ✅ Load dữ liệu động từ JSON

## 📁 Cấu Trúc

```
huonggiang/
├── ⚡ FlashSale Shopee.html    # Template HTML gốc
├── index.html                   # File deploy lên GitHub Pages
├── data/
│   └── products.json            # Dữ liệu sản phẩm (với affiliate links)
├── generate_index.py            # Script tạo index.html (hardcode JSON)
└── generate_index_fetch.py      # Script tạo index.html (Fetch API)
```

## � Cách Sử Dụng

### Phương Án 1: Hardcode JSON (Khuyến nghị cho GitHub Pages)

**Ưu điểm:** Chỉ cần deploy 1 file, load nhanh, không CORS issues

```bash
# 1. Tạo index.html
python generate_index.py

# 2. Test local
python -m http.server 8000
# Mở: http://localhost:8000/

# 3. Deploy
git add index.html
git commit -m "🚀 Deploy website"
git push
```

### Phương Án 2: Fetch API (Linh hoạt, dễ cập nhật)

**Ưu điểm:** File HTML nhỏ, dễ cập nhật dữ liệu

```bash
# 1. Tạo index.html với Fetch API
python generate_index_fetch.py

# 2. Test local (BẮT BUỘC dùng web server)
python -m http.server 8000
# Mở: http://localhost:8000/

# 3. Deploy (cần cả 2 files)
git add index.html data/products.json
git commit -m "🚀 Deploy website"
git push
```

## 📊 Workflow Cập Nhật Dữ Liệu

### Nếu đã có file `products.json` sẵn:

```bash
# Tạo index.html mới
python generate_index.py

# Deploy
git add index.html
git commit -m "🔄 Update products"
git push
```

### Nếu cần thu thập dữ liệu mới:

```bash
# 1. Thu thập từ dealhotday.com (từ thư mục gốc)
cd ..
python main.py --stage 1

# 2. Upload Excel lên Shopee Affiliate Portal
# → Tải về converted_links.csv

# 3. Merge affiliate links
python main.py --stage 2

# 4. Xuất JSON
python main.py --stage 3

# 5. Copy JSON sang thư mục huonggiang
copy data\products.json huonggiang\data\products.json

# 6. Tạo index.html
cd huonggiang
python generate_index.py

# 7. Deploy
git add index.html
git commit -m "🔄 Update products"
git push
```

## 🌐 Deploy Lên GitHub Pages

### Lần Đầu Tiên

1. **Tạo repository trên GitHub**
2. **Push code:**
   ```bash
   git init
   git add index.html
   git commit -m "🚀 Initial deployment"
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

3. **Kích hoạt GitHub Pages:**
   - Vào repository → Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`, Folder: `/ (root)`
   - Save

4. **Truy cập website:**
   ```
   https://YOUR_USERNAME.github.io/REPO_NAME/
   ```

### Cập Nhật Sau Này

```bash
# Tạo index.html mới
python generate_index.py

# Deploy
git add index.html
git commit -m "🔄 Update $(date +%Y-%m-%d)"
git push

# Website tự động cập nhật sau 1-2 phút
```

## 🔧 Scripts Hỗ Trợ

### `generate_index.py`

Tạo `index.html` với dữ liệu hardcode từ `products.json`.

**Cách dùng:**
```bash
python generate_index.py
```

**Kết quả:**
- File `index.html` chứa toàn bộ dữ liệu sản phẩm
- Sẵn sàng deploy lên GitHub Pages
- Chỉ cần deploy 1 file

### `generate_index_fetch.py`

Tạo `index.html` load dữ liệu động từ `data/products.json` bằng Fetch API.

**Cách dùng:**
```bash
python generate_index_fetch.py
```

**Kết quả:**
- File `index.html` nhỏ gọn
- Load dữ liệu từ `data/products.json`
- Cần deploy cả 2 files: `index.html` + `data/products.json`

**Lưu ý:**
- ⚠️ KHÔNG test được bằng `file://` (CORS error)
- ✅ PHẢI dùng web server: `python -m http.server 8000`

### `update_html.py`

Cập nhật file HTML gốc `⚡ FlashSale Shopee.html` với dữ liệu mới.

**Cách dùng:**
```bash
python update_html.py
```

## 📝 File `products.json`

### Cấu Trúc

```json
[
  {
    "shopid": 123456,
    "name": "Tên sản phẩm",
    "discount": 50,
    "rating_count": 1234,
    "is_mall": true,
    "is_preferred": false,
    "is_preferred_plus": false,
    "price": 99,
    "raw_price": 99000.0,
    "before": 199000.0,
    "rating": 4.8,
    "stock": 100,
    "img": "https://cf.shopee.vn/file/...",
    "url": "https://s.shopee.vn/...",
    "raw": { ... }
  }
]
```

### Nguồn Dữ Liệu

- **Thu thập tự động:** Từ dealhotday.com (dùng hệ thống Python ở thư mục gốc)
- **Thủ công:** Tạo file JSON theo format trên

## 🎨 Tùy Chỉnh Giao Diện

### Sửa Template

1. Mở file `⚡ FlashSale Shopee.html`
2. Chỉnh sửa CSS, HTML theo ý muốn
3. Chạy lại script generate để tạo `index.html` mới

### Thay Đổi Màu Sắc

Tìm và sửa trong CSS:
- `#ee4d2d` - Màu chủ đạo (đỏ Shopee)
- `#d0011b` - Màu Shop Mall
- `#1da1f2` - Màu nút Telegram

## � Troubleshooting

### Website không hiển thị sản phẩm

**Kiểm tra:**
1. Mở Console (F12) xem có lỗi không
2. Kiểm tra file `products.json` có tồn tại không
3. Nếu dùng Fetch API, đảm bảo test bằng web server

### Lỗi CORS khi dùng Fetch API

**Nguyên nhân:** Đang test bằng `file://` protocol

**Giải pháp:**
```bash
python -m http.server 8000
# Mở: http://localhost:8000/
```

### Website không cập nhật sau khi push

**Giải pháp:**
1. Clear cache: Ctrl + Shift + R
2. Đợi 2-3 phút để GitHub Pages rebuild
3. Kiểm tra deployment status trên GitHub

## 📊 So Sánh 2 Phương Pháp

| Tiêu chí | Hardcode JSON | Fetch API |
|----------|---------------|-----------|
| Số file deploy | 1 file | 2 files |
| Kích thước HTML | Lớn (~6MB) | Nhỏ (~100KB) |
| Tốc độ load | Nhanh (1 request) | Chậm hơn (2 requests) |
| Dễ cập nhật | Phải tạo lại HTML | Chỉ cần thay JSON |
| CORS issues | Không | Có (khi test local) |
| Test local | Mở file trực tiếp | Cần web server |
| **Khuyến nghị** | ✅ GitHub Pages | ✅ Server riêng |

## � Liên Hệ

- Telegram: https://t.me/dealhotday
- Website: https://dealhotday.com

## 📝 License

MIT License

---

**Cập nhật lần cuối:** 2026-01-16
