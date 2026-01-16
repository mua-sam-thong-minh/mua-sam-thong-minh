"""
Parser Module - Trích xuất và parse dữ liệu JSON từ HTML
"""
import re
import json
from typing import List, Dict, Optional


def extract_products_from_html(html: str) -> List[Dict]:
    """
    Trích xuất danh sách sản phẩm từ HTML
    
    Args:
        html: HTML content từ dealhotday.com
    
    Returns:
        List các product dict với shopid, itemid, name, price, etc.
        
    Raises:
        ValueError: Khi không tìm thấy dữ liệu hoặc JSON không hợp lệ
    """
    print("🔍 Đang tìm kiếm dữ liệu ITEMS trong HTML...")
    
    # Pattern 1: const ITEMS = [...]
    pattern1 = r'const ITEMS = (\[.*?\]);'
    match = re.search(pattern1, html, re.DOTALL)
    
    if not match:
        # Pattern 2: var ITEMS = [...]
        pattern2 = r'var ITEMS = (\[.*?\]);'
        match = re.search(pattern2, html, re.DOTALL)
    
    if not match:
        raise ValueError(
            "Không tìm thấy dữ liệu ITEMS trong HTML. "
            "Có thể cấu trúc trang web đã thay đổi."
        )
    
    json_str = match.group(1)
    print(f"✅ Tìm thấy dữ liệu JSON, kích thước: {len(json_str):,} bytes")
    
    try:
        products = json.loads(json_str)
        print(f"✅ Parse JSON thành công: {len(products)} sản phẩm")
    except json.JSONDecodeError as e:
        raise ValueError(f"Lỗi parse JSON: {e}")
    
    # Validate và lọc sản phẩm
    valid_products = []
    invalid_count = 0
    
    for i, product in enumerate(products):
        if validate_product(product):
            valid_products.append(product)
        else:
            invalid_count += 1
            print(f"⚠️  Sản phẩm #{i+1} không hợp lệ, bỏ qua")
    
    print(f"✅ Có {len(valid_products)} sản phẩm hợp lệ")
    if invalid_count > 0:
        print(f"⚠️  Đã bỏ qua {invalid_count} sản phẩm không hợp lệ")
    
    return valid_products


def validate_product(product: Dict) -> bool:
    """
    Kiểm tra tính hợp lệ của sản phẩm
    
    Args:
        product: Product dict
    
    Returns:
        True nếu sản phẩm hợp lệ
    """
    required_fields = ['shopid', 'name', 'raw']
    
    # Kiểm tra các trường bắt buộc
    for field in required_fields:
        if field not in product:
            return False
    
    # Kiểm tra raw.itemid
    if 'itemid' not in product['raw']:
        return False
    
    # Kiểm tra shopid và itemid là số
    try:
        int(product['shopid'])
        int(product['raw']['itemid'])
    except (ValueError, TypeError):
        return False
    
    return True


def extract_product_info(product: Dict) -> Dict:
    """
    Trích xuất thông tin quan trọng từ product dict
    
    Args:
        product: Product dict từ JSON
    
    Returns:
        Dict chứa thông tin đã được làm sạch
    """
    return {
        'shopid': product['shopid'],
        'itemid': product['raw']['itemid'],
        'name': product.get('name', ''),
        'price': product.get('price', 0),
        'raw_price': product.get('raw_price', 0),
        'before': product.get('before', 0),
        'discount': product.get('discount', 0),
        'rating': product.get('rating', 0),
        'rating_count': product.get('rating_count', 0),
        'stock': product.get('stock', 0),
        'img': product.get('img', ''),
        'is_mall': product.get('is_mall', False),
        'is_preferred': product.get('is_preferred', False),
        'is_preferred_plus': product.get('is_preferred_plus', False),
        'url': product.get('url', ''),  # Link affiliate cũ (sẽ được thay thế)
    }


def get_statistics(products: List[Dict]) -> Dict:
    """
    Tính toán thống kê về danh sách sản phẩm
    
    Args:
        products: Danh sách sản phẩm
    
    Returns:
        Dict chứa các thống kê
    """
    if not products:
        return {}
    
    mall_count = sum(1 for p in products if p.get('is_mall', False))
    preferred_count = sum(1 for p in products if p.get('is_preferred', False))
    
    discounts = [p.get('discount', 0) for p in products]
    prices = [p.get('price', 0) for p in products]
    
    return {
        'total': len(products),
        'mall': mall_count,
        'preferred': preferred_count,
        'avg_discount': sum(discounts) / len(discounts) if discounts else 0,
        'avg_price': sum(prices) / len(prices) if prices else 0,
        'max_discount': max(discounts) if discounts else 0,
        'min_price': min(prices) if prices else 0,
    }


if __name__ == "__main__":
    # Test module
    test_html = """
    <script>
        const ITEMS = [
            {
                "shopid": 123456,
                "name": "Test Product",
                "price": 1000,
                "raw": {"itemid": 789012}
            }
        ];
    </script>
    """
    
    try:
        products = extract_products_from_html(test_html)
        print(f"✅ Test thành công: {len(products)} sản phẩm")
        
        stats = get_statistics(products)
        print(f"📊 Thống kê: {stats}")
    except Exception as e:
        print(f"❌ Test thất bại: {e}")
