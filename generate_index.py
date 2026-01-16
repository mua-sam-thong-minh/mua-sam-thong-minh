"""
Script Tạo index.html Cho GitHub Pages
Tự động tạo file index.html hoàn chỉnh từ products.json và HTML template
"""

# Fix encoding cho Windows console
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
from pathlib import Path
from datetime import datetime
import shutil


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
        "img": product.get('image', product.get('img', '')),
        "url": product.get('link', product.get('url', '')),
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


def generate_index_html(products_json_path, template_html_path, output_path):
    """
    Tạo file index.html từ template và products.json
    
    Args:
        products_json_path: Đường dẫn file products.json
        template_html_path: Đường dẫn file HTML template
        output_path: Đường dẫn file index.html output
    """
    
    # 1. Đọc products.json
    print(f"📖 Đang đọc {products_json_path}...")
    with open(products_json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"✅ Đã load {len(products)} sản phẩm")
    
    # 2. Tạo JSON string trực tiếp từ dữ liệu gốc (không convert)
    print("🔄 Đang tạo JSON string...")
    items_json = json.dumps(products, ensure_ascii=False, indent=20)
    
    # 3. Đọc template HTML
    print(f"📖 Đang đọc template {template_html_path}...")
    with open(template_html_path, 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # 4. Thay thế const ITEMS = [...] trong template
    import re
    pattern = r'const ITEMS = \[.*?\];'
    
    # Sử dụng lambda để tránh lỗi escape sequence trong replacement string
    def replace_items(match):
        return f'const ITEMS = {items_json};'
    
    html_content = re.sub(pattern, replace_items, html_template, flags=re.DOTALL)
    
    # 5. Thêm comment BUILD_ID
    build_id = datetime.now().strftime('%Y%m%d%H%M%S')
    html_content = html_content.replace(
        '<!-- BUILD_ID:',
        f'<!-- BUILD_ID: {build_id} -->\n    <!-- ORIGINAL BUILD_ID:'
    )
    
    # 6. Lưu file index.html
    print(f"💾 Đang tạo {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ TẠO FILE THÀNH CÔNG!")
    print(f"📁 File output: {output_path}")
    print(f"📊 Số sản phẩm: {len(products)}")
    print(f"🔖 Build ID: {build_id}")
    
    return True


def main():
    """Main function"""
    
    # Đường dẫn files
    products_file = Path("data/products.json")
    template_file = Path("⚡ FlashSale Shopee.html")
    output_file = Path("index.html")  # File cho GitHub Pages
    
    # Kiểm tra files
    if not products_file.exists():
        print(f"❌ Lỗi: Không tìm thấy {products_file}")
        print("   Hãy chạy: python main.py --stage 3")
        return
    
    if not template_file.exists():
        print(f"❌ Lỗi: Không tìm thấy template HTML: {template_file}")
        return
    
    # Banner
    print("="*70)
    print("🚀 TẠO FILE INDEX.HTML CHO GITHUB PAGES")
    print("="*70)
    print()
    
    # Generate
    success = generate_index_html(products_file, template_file, output_file)
    
    if success:
        print("\n" + "="*70)
        print("✅ HOÀN TẤT! File index.html đã sẵn sàng")
        print("="*70)
        print("\n📋 BƯỚC TIẾP THEO:")
        print("\n1. Test local:")
        print("   python -m http.server 8000")
        print("   → Mở http://localhost:8000/")
        print("\n2. Deploy lên GitHub:")
        print("   git add index.html")
        print("   git commit -m '🚀 Deploy FlashSale website'")
        print("   git push")
        print("\n3. Kích hoạt GitHub Pages:")
        print("   → Vào Settings → Pages")
        print("   → Source: Deploy from branch")
        print("   → Branch: main, Folder: / (root)")
        print("\n4. Truy cập website:")
        print("   → https://YOUR_USERNAME.github.io/AFF_SHOPPE/")
        print()


if __name__ == "__main__":
    main()
