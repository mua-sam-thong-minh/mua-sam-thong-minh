"""
Script Tạo index.html Với Fetch API
Tạo file index.html load dữ liệu từ products.json bằng Fetch API
"""

# Fix encoding cho Windows console
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import json
from pathlib import Path
from datetime import datetime
import re


def generate_index_with_fetch(template_html_path, output_path):
    """
    Tạo file index.html với Fetch API để load products.json
    
    Args:
        template_html_path: Đường dẫn file HTML template
        output_path: Đường dẫn file index.html output
    """
    
    # 1. Đọc template HTML
    print(f"📖 Đang đọc template {template_html_path}...")
    with open(template_html_path, 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # 2. Tạo code Fetch API
    fetch_code = """let ITEMS = [];

async function loadProducts() {
  try {
    const response = await fetch('data/products.json');
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    ITEMS = await response.json();
    console.log(`✅ Loaded ${ITEMS.length} products`);
    
    // Render products after loading
    if (typeof renderProducts === 'function') {
      renderProducts();
    } else if (typeof init === 'function') {
      init();
    }
  } catch (error) {
    console.error('❌ Error loading products:', error);
    document.body.innerHTML = `
      <div style="text-align: center; padding: 50px; font-family: Arial;">
        <h2>⚠️ Không thể tải dữ liệu sản phẩm</h2>
        <p>Vui lòng thử lại sau hoặc liên hệ admin.</p>
        <p style="color: #999; font-size: 0.9em;">Error: ${error.message}</p>
      </div>
    `;
  }
}

// Load when page is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadProducts);
} else {
  loadProducts();
}"""
    
    # 3. Thay thế const ITEMS = [...] bằng Fetch API code
    pattern = r'const ITEMS = \[.*?\];'
    
    html_content = re.sub(pattern, fetch_code, html_template, flags=re.DOTALL)
    
    # 4. Thêm comment BUILD_ID
    build_id = datetime.now().strftime('%Y%m%d%H%M%S')
    html_content = html_content.replace(
        '<!-- BUILD_ID:',
        f'<!-- BUILD_ID: {build_id} (Fetch API) -->\n    <!-- ORIGINAL BUILD_ID:'
    )
    
    # 5. Lưu file index.html
    print(f"💾 Đang tạo {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ TẠO FILE THÀNH CÔNG!")
    print(f"📁 File output: {output_path}")
    print(f"🔖 Build ID: {build_id}")
    print(f"📡 Load method: Fetch API (dynamic)")
    
    return True


def main():
    """Main function"""
    
    # Đường dẫn files
    template_file = Path("⚡ FlashSale Shopee.html")
    output_file = Path("index.html")  # File cho GitHub Pages
    
    # Kiểm tra files
    if not template_file.exists():
        print(f"❌ Lỗi: Không tìm thấy template HTML: {template_file}")
        return
    
    # Banner
    print("="*70)
    print("🚀 TẠO FILE INDEX.HTML VỚI FETCH API")
    print("="*70)
    print()
    
    # Generate
    success = generate_index_with_fetch(template_file, output_file)
    
    if success:
        print("\n" + "="*70)
        print("✅ HOÀN TẤT! File index.html đã sẵn sàng")
        print("="*70)
        print("\n📋 BƯỚC TIẾP THEO:")
        print("\n1. Copy file products.json:")
        print("   copy data\\products.json data\\products.json")
        print("\n2. Test local (BẮT BUỘC dùng web server):")
        print("   python -m http.server 8000")
        print("   → Mở http://localhost:8000/")
        print("\n3. Deploy lên GitHub:")
        print("   git add index.html data/products.json")
        print("   git commit -m '🚀 Deploy FlashSale website'")
        print("   git push")
        print("\n⚠️ LƯU Ý:")
        print("   - KHÔNG thể test bằng file:// (CORS error)")
        print("   - PHẢI dùng web server để test")
        print("   - Cần deploy CẢ index.html VÀ data/products.json")
        print()


if __name__ == "__main__":
    main()
