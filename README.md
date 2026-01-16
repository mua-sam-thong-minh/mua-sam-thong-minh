# 🚀 Hệ Thống Thu Thập & Chuyển Đổi Link Affiliate Shopee

Hệ thống tự động thu thập dữ liệu FlashSale từ dealhotday.com, chuyển đổi thành link affiliate Shopee của bạn, và tự động cập nhật lên website.

## 📋 Tính Năng

- ✅ Thu thập dữ liệu FlashSale tự động từ dealhotday.com
- ✅ Tái tạo link gốc Shopee từ shopid/itemid
- ✅ Tích hợp với Shopee Affiliate Portal
- ✅ Xuất JSON tự động cho website
- ✅ Hỗ trợ batch processing hàng trăm sản phẩm

## 🛠️ Cài Đặt

### 1. Yêu cầu hệ thống
- Python 3.8+
- pip

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình (Optional)

Sao chép file `.env.example` thành `.env` và điều chỉnh nếu cần:

```bash
copy .env.example .env
```

## 📖 Hướng Dẫn Sử Dụng

Hệ thống hoạt động theo 3 giai đoạn:

### Giai đoạn 1: Thu thập & Sơ chế dữ liệu

```bash
python main.py --stage 1
```

**Kết quả:**
- File `data/input_links_YYYYMMDD_HHMMSS.csv` (chi tiết)
- File `data/input_links_simple_YYYYMMDD_HHMMSS.csv` (để upload lên Shopee)

**Tùy chọn:**
```bash
# Chỉ định ngày và giờ cụ thể
python main.py --stage 1 --date 16.01.2026 --time 17.00
```

### Giai đoạn 2: Chuyển đổi Link Affiliate

**Bước thủ công:**
1. Mở file `input_links_simple_*.csv`
2. Truy cập [Shopee Affiliate Portal](https://affiliate.shopee.vn)
3. Tìm chức năng "Link Converter" hoặc "Batch Convert"
4. Upload file CSV
5. Tải file kết quả về và lưu vào `data/converted_links.csv`

**Chạy merge:**
```bash
python main.py --stage 2
```

### Giai đoạn 3: Xuất JSON & Deploy

```bash
python main.py --stage 3
```

**Kết quả:**
- File `data/products.json` - Dữ liệu cuối cùng cho website

**Deploy lên website:**
```bash
git add data/products.json
git commit -m "🔄 Update FlashSale products"
git push
```

## 📁 Cấu Trúc Dự Án

```
AFF_SHOPPE/
├── src/
│   ├── fetcher.py          # Thu thập dữ liệu từ dealhotday.com
│   ├── parser.py           # Parse HTML/JSON
│   ├── link_builder.py     # Tái tạo link gốc Shopee
│   ├── exporter.py         # Xuất CSV
│   ├── merger.py           # Merge link affiliate
│   └── json_generator.py   # Xuất JSON cuối cùng
├── data/
│   ├── input_links_*.csv       # Output Giai đoạn 1
│   ├── converted_links.csv     # Input Giai đoạn 2 (manual)
│   └── products.json           # Output cuối cùng
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md              # File này
```

## 🔧 Troubleshooting

### Lỗi: "Không tìm thấy dữ liệu ITEMS"
- Kiểm tra URL có đúng không
- Thử với khung giờ khác
- Kiểm tra kết nối internet

### Lỗi: "Không tìm thấy file converted_links.csv"
- Đảm bảo đã upload file CSV lên Shopee Affiliate Portal
- Tải file kết quả về và lưu đúng tên: `data/converted_links.csv`

### Lỗi: Request bị chặn (403/429)
- Tăng `REQUEST_DELAY` trong file `.env`
- Thử lại sau vài phút

## 📊 Ví Dụ Workflow Hoàn Chỉnh

```bash
# Bước 1: Thu thập dữ liệu
python main.py --stage 1

# Bước 2: Upload CSV lên Shopee, tải về converted_links.csv

# Bước 3: Merge link affiliate
python main.py --stage 2

# Bước 4: Xuất JSON
python main.py --stage 3

# Bước 5: Deploy
git add data/products.json
git commit -m "🔄 Update FlashSale products $(date)"
git push
```

## 🤝 Đóng Góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.

## 📝 License

MIT License

