"""
Exporter Module - Xuất dữ liệu ra CSV
"""
import csv
from typing import List, Dict
import os
import pandas as pd


def export_links_to_csv(products: List[Dict], output_path: str) -> None:
    """
    Xuất danh sách link gốc ra CSV
    
    Args:
        products: Danh sách sản phẩm (phải có trường 'original_link')
        output_path: Đường dẫn file CSV output
    """
    print(f"📝 Đang xuất {len(products)} link ra CSV...")
    
    # Tạo thư mục nếu chưa có
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow([
            'Link Gốc',
            'Tên Sản Phẩm',
            'ShopID',
            'ItemID',
            'Giá (VNĐ)',
            'Giảm giá (%)',
            'Shop Mall',
            'Đánh giá'
        ])
        
        # Data rows
        for product in products:
            writer.writerow([
                product.get('original_link', ''),
                product.get('name', ''),
                product.get('shopid', ''),
                product.get('itemid', ''),
                product.get('price', 0),
                product.get('discount', 0),
                'Có' if product.get('is_mall', False) else 'Không',
                f"{product.get('rating', 0):.2f} ({product.get('rating_count', 0)} đánh giá)"
            ])
    
    file_size = os.path.getsize(output_path)
    print(f"✅ Đã xuất file: {output_path}")
    print(f"📦 Kích thước: {file_size:,} bytes")


def export_simple_links_xlsx(products: List[Dict], output_path: str) -> None:
    """
    Xuất file Excel (.xlsx) để upload lên Shopee Affiliate
    Format: 6 cột - "Liên kết gốc", "Sub_id1", "Sub_id2", "Sub_id3", "Sub_id4", "Sub_id5"
    
    Args:
        products: Danh sách sản phẩm
        output_path: Đường dẫn file .xlsx output
    """
    print(f"📝 Đang xuất file Excel cho Shopee Affiliate...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Tạo DataFrame với 6 cột
    data = {
        'Liên kết gốc': [p.get('original_link', '') for p in products],
        'Sub_id1': [''] * len(products),
        'Sub_id2': [''] * len(products),
        'Sub_id3': [''] * len(products),
        'Sub_id4': [''] * len(products),
        'Sub_id5': [''] * len(products)
    }
    
    df = pd.DataFrame(data)
    
    # Xuất ra file Excel
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    print(f"✅ Đã xuất file: {output_path}")
    print(f"📦 Tổng số link: {len(products)}")
    print(f"📋 Format: Excel (.xlsx) với 6 cột (Liên kết gốc + 5 Sub_id)")
    print(f"\n💡 Hướng dẫn:")
    print(f"   1. Truy cập: https://affiliate.shopee.vn/offer/custom_link")
    print(f"   2. Click 'Tải lên file' hoặc 'Upload file'")
    print(f"   3. Chọn file: {output_path}")
    print(f"   4. Tải file kết quả về và lưu vào: data/converted_links.csv")


if __name__ == "__main__":
    # Test module
    test_products = [
        {
            'original_link': 'https://shopee.vn/product/123/456',
            'name': 'Test Product 1',
            'shopid': 123,
            'itemid': 456,
            'price': 1000,
            'discount': 50,
            'is_mall': True,
            'rating': 4.5,
            'rating_count': 100
        }
    ]
    
    try:
        export_links_to_csv(test_products, 'data/test_output.csv')
        print("✅ Test thành công")
    except Exception as e:
        print(f"❌ Test thất bại: {e}")
