"""
JSON Generator Module - Xuất dữ liệu cuối cùng ra JSON (Giai đoạn 3)
"""
import json
import os
from typing import List, Dict
from datetime import datetime


def generate_final_json(products: List[Dict], output_path: str, metadata: Dict = None) -> None:
    """
    Xuất dữ liệu cuối cùng ra JSON
    
    Args:
        products: Danh sách sản phẩm đã có link affiliate
        output_path: Đường dẫn file JSON output
        metadata: Metadata bổ sung (optional)
    """
    print(f"\n📦 Đang tạo file JSON cuối cùng...")
    
    # Tạo thư mục nếu chưa có
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Chuẩn bị dữ liệu
    output_data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_products': len(products),
            'version': '1.0',
            **(metadata or {})
        },
        'products': products
    }
    
    # Xuất JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ Đã tạo file: {output_path}")
    print(f"📦 Kích thước: {file_size:,} bytes")
    print(f"📊 Số sản phẩm: {len(products)}")


def generate_products_only_json(products: List[Dict], output_path: str) -> None:
    """
    Xuất JSON chỉ chứa array sản phẩm (tương thích với HTML hiện tại)
    
    Args:
        products: Danh sách sản phẩm
        output_path: Đường dẫn file JSON output
    """
    print(f"\n📦 Đang tạo file products.json...")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ Đã tạo file: {output_path}")
    print(f"📦 Kích thước: {file_size:,} bytes")
    print(f"📊 Số sản phẩm: {len(products)}")


def validate_json_output(json_path: str) -> bool:
    """
    Kiểm tra tính hợp lệ của file JSON output
    
    Args:
        json_path: Đường dẫn file JSON
    
    Returns:
        True nếu JSON hợp lệ
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            # Format array
            print(f"✅ JSON hợp lệ: {len(data)} sản phẩm")
            return True
        elif isinstance(data, dict) and 'products' in data:
            # Format object với metadata
            print(f"✅ JSON hợp lệ: {len(data['products'])} sản phẩm")
            return True
        else:
            print("❌ JSON không đúng format")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi validate JSON: {e}")
        return False


if __name__ == "__main__":
    # Test module
    test_products = [
        {
            'shopid': 123,
            'name': 'Test Product',
            'price': 1000,
            'url': 'https://s.shopee.vn/test'
        }
    ]
    
    try:
        generate_products_only_json(test_products, 'data/test_products.json')
        
        if validate_json_output('data/test_products.json'):
            print("✅ Test thành công")
        
        # Cleanup
        if os.path.exists('data/test_products.json'):
            os.remove('data/test_products.json')
            
    except Exception as e:
        print(f"❌ Test thất bại: {e}")
