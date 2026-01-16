"""
Script Tự Động Update HTML
Tự động thay thế dữ liệu ITEMS trong file HTML bằng dữ liệu mới từ products.json
"""

import json
import re
from pathlib import Path
import shutil
from datetime import datetime


def convert_product_to_html_format(product):
    """Convert product sang format HTML"""
    display_price = round(product.get('price', 0) / 1000)
    
    return {
        "shopid": product.get('shopid', 0),
        "name": product.get('name', ''),
        "discount": product.get('discount', 0),
        "rating_count": product.get('rating_count', 0),
        "is_mall": product.get('is_mall', False),
        "is_preferred": product.get('is_preferred', False),
        "is_preferred_plus": product.get('is_preferred_plus', False),
        "price": display_price,
        "raw_price": float(product.get('price', 0)),
        "before": float(product.get('original_price', 0)),
        "rating": product.get('rating', 0.0),
        "stock": product.get('stock', 0),
        "img": product.get('image', ''),
        "url": product.get('link', product.get('original_link', '')),
        "raw": {
            "itemid": product.get('itemid', 0),
            "shopid": product.get('shopid', 0),
            "name": product.get('name', ''),
            "url": product.get('link', product.get('original_link', '')),
            "is_shop_official": product.get('is_mall', False),
            "is_shop_preferred": product.get('is_preferred', False),
            "is_shop_preferred_plus": product.get('is_preferred_plus', False),
            "item_rating": {
                "rating_star": product.get('rating', 0.0),
                "rating_counts": [product.get('rating_count', 0), 0, 0, 0, 0, 0]
            }
        }
    }


def update_html_file(html_path, products_json_path):
    """
    Tự động update file HTML với dữ liệu mới
    
    Args:
        html_path: Đường dẫn file HTML
        products_json_path: Đường dẫn file products.json
    """
    
    # 1. Đọc dữ liệu products.json
    print(f"📖 Đang đọc {products_json_path}...")
    with open(products_json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"✅ Đã load {len(products)} sản phẩm")
    
    # 2. Convert sang format HTML
    print("🔄 Đang convert sang format HTML...")
    html_products = [convert_product_to_html_format(p) for p in products]
    
    # 3. Tạo JSON string với indent đẹp
    items_json = json.dumps(html_products, ensure_ascii=False, indent=20)
    
    # 4. Đọc file HTML
    print(f"📖 Đang đọc {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 5. Backup file HTML
    backup_path = html_path.parent / f"{html_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{html_path.suffix}"
    print(f"💾 Backup file HTML → {backup_path.name}")
    shutil.copy2(html_path, backup_path)
    
    # 6. Tìm và thay thế const ITEMS = [...]
    # Pattern: const ITEMS = [...]; (bao gồm cả dấu ; cuối)
    pattern = r'const ITEMS = \[.*?\];'
    
    # Tạo replacement string
    replacement = f'const ITEMS = {items_json};'
    
    # Thay thế (DOTALL để match qua nhiều dòng)
    new_html_content, count = re.subn(pattern, replacement, html_content, flags=re.DOTALL)
    
    if count == 0:
        print("❌ Lỗi: Không tìm thấy 'const ITEMS = [...]' trong file HTML")
        print("   Vui lòng kiểm tra lại cấu trúc file HTML")
        return False
    
    # 7. Lưu file HTML mới
    print(f"💾 Đang lưu file HTML đã cập nhật...")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    
    print(f"\n✅ CẬP NHẬT THÀNH CÔNG!")
    print(f"📁 File HTML: {html_path}")
    print(f"📊 Số sản phẩm: {len(html_products)}")
    print(f"💾 Backup: {backup_path.name}")
    
    return True


def main():
    """Main function"""
    # Đường dẫn files
    html_file = Path("huonggiang/⚡ FlashSale Shopee.html")
    products_file = Path("data/products.json")
    
    # Kiểm tra file tồn tại
    if not html_file.exists():
        print(f"❌ Lỗi: Không tìm thấy file HTML: {html_file}")
        return
    
    if not products_file.exists():
        print(f"❌ Lỗi: Không tìm thấy file products.json: {products_file}")
        print("   Hãy chạy: python main.py --stage 3")
        return
    
    # Update HTML
    print("="*70)
    print("🚀 TỰ ĐỘNG CẬP NHẬT FILE HTML")
    print("="*70)
    print()
    
    success = update_html_file(html_file, products_file)
    
    if success:
        print("\n" + "="*70)
        print("✅ HOÀN TẤT! Website đã sẵn sàng deploy")
        print("="*70)
        print("\n📋 BƯỚC TIẾP THEO:")
        print("   1. Mở file HTML trong browser để kiểm tra")
        print("   2. Commit và push lên GitHub:")
        print("      git add '⚡ FlashSale Shopee.html'")
        print("      git commit -m '🔄 Update products'")
        print("      git push")


if __name__ == "__main__":
    main()
