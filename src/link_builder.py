"""
Link Builder Module - Tái tạo link gốc Shopee từ shopid và itemid
"""
from typing import List, Dict


def build_original_link(shopid: int, itemid: int) -> str:
    """
    Tái tạo link gốc Shopee
    
    Args:
        shopid: ID của shop
        itemid: ID của sản phẩm
    
    Returns:
        URL gốc dạng https://shopee.vn/product/{shopid}/{itemid}
    
    Examples:
        >>> build_original_link(1378403879, 24090213840)
        'https://shopee.vn/product/1378403879/24090213840'
    """
    return f"https://shopee.vn/product/{shopid}/{itemid}"


def build_links_for_products(products: List[Dict]) -> List[Dict]:
    """
    Tạo link gốc cho tất cả sản phẩm
    
    Args:
        products: Danh sách sản phẩm
    
    Returns:
        Danh sách sản phẩm đã có thêm trường 'original_link'
    """
    print(f"🔗 Đang tạo link gốc cho {len(products)} sản phẩm...")
    
    for product in products:
        shopid = product['shopid']
        itemid = product['raw']['itemid']
        product['original_link'] = build_original_link(shopid, itemid)
    
    print("✅ Hoàn tất tạo link gốc")
    return products


def validate_link_format(link: str) -> bool:
    """
    Kiểm tra format của link Shopee
    
    Args:
        link: URL cần kiểm tra
    
    Returns:
        True nếu link đúng format
    """
    import re
    pattern = r'^https://shopee\.vn/product/\d+/\d+$'
    return bool(re.match(pattern, link))


if __name__ == "__main__":
    # Test module
    test_cases = [
        (1378403879, 24090213840),
        (468090373, 24709582664),
        (163471961, 5362683985),
    ]
    
    print("🧪 Testing link builder...")
    for shopid, itemid in test_cases:
        link = build_original_link(shopid, itemid)
        is_valid = validate_link_format(link)
        status = "✅" if is_valid else "❌"
        print(f"{status} {link}")
