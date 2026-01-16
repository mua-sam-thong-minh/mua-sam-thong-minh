"""
Merger Module - Ghép link affiliate vào dữ liệu sản phẩm (Giai đoạn 2)
"""
import csv
import pandas as pd
from typing import List, Dict
import os


def read_converted_links_csv(csv_path: str) -> Dict[str, str]:
    """
    Đọc file CSV chứa link đã convert từ Shopee Affiliate
    
    Args:
        csv_path: Đường dẫn file converted_links.csv
    
    Returns:
        Dict mapping {link_gốc: link_affiliate}
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Không tìm thấy file {csv_path}. "
            "Vui lòng upload file converted_links.csv từ Shopee Affiliate Portal."
        )
    
    print(f"📖 Đang đọc file {csv_path}...")
    
    link_map = {}
    
    try:
        # Đọc CSV với encoding UTF-8 (Shopee dùng UTF-8)
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        print(f"📋 Các cột trong file: {df.columns.tolist()}")
        
        # Shopee Affiliate format: "Liên kết gốc", "Liên kết chuyển đổi"
        # Hoặc có thể là: "Link Gốc", "Link Affiliate"
        original_col = None
        converted_col = None
        
        # Tìm cột chứa link gốc
        for col in df.columns:
            col_lower = col.lower().strip()
            if 'liên kết gốc' in col_lower or 'link gốc' in col_lower or 'original' in col_lower:
                original_col = col
            elif 'liên kết chuyển đổi' in col_lower or 'link affiliate' in col_lower or 'converted' in col_lower or 'chuyển đổi' in col_lower:
                converted_col = col
        
        # Fallback: nếu không tìm thấy, dùng 2 cột đầu tiên
        if original_col is None or converted_col is None:
            if len(df.columns) >= 2:
                original_col = df.columns[0]
                converted_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
                print(f"⚠️  Không tìm thấy tên cột chuẩn, sử dụng: '{original_col}' và '{converted_col}'")
            else:
                raise ValueError(
                    f"File CSV phải có ít nhất 2 cột. "
                    f"Hiện tại có: {df.columns.tolist()}"
                )
        
        print(f"✅ Sử dụng cột: '{original_col}' -> '{converted_col}'")
        
        # Tạo mapping, bỏ qua các dòng trống
        for idx, row in df.iterrows():
            orig = str(row[original_col]).strip()
            conv = str(row[converted_col]).strip()
            
            # Bỏ qua nếu link trống hoặc NaN
            if orig and conv and orig != 'nan' and conv != 'nan':
                link_map[orig] = conv
        
        print(f"✅ Đã đọc {len(link_map)} link mapping")
        
    except Exception as e:
        print(f"❌ Lỗi khi đọc CSV: {e}")
        raise
    
    return link_map


def merge_affiliate_links(products: List[Dict], csv_path: str) -> List[Dict]:
    """
    Ghép link affiliate vào dữ liệu sản phẩm
    
    Args:
        products: Danh sách sản phẩm từ Giai đoạn 1
        csv_path: Đường dẫn file converted_links.csv
    
    Returns:
        Danh sách sản phẩm đã có link affiliate mới
    """
    print(f"\n🔗 Bắt đầu merge link affiliate...")
    
    link_map = read_converted_links_csv(csv_path)
    
    matched_count = 0
    unmatched_count = 0
    
    for product in products:
        original_link = product.get('original_link', '')
        
        if original_link in link_map:
            # Thay thế link affiliate
            new_affiliate_link = link_map[original_link]
            product['url'] = new_affiliate_link
            if 'raw' in product:
                product['raw']['url'] = new_affiliate_link
            matched_count += 1
        else:
            unmatched_count += 1
            print(f"⚠️  Không tìm thấy link affiliate cho: {original_link}")
    
    print(f"\n✅ Merge hoàn tất:")
    print(f"   - Matched: {matched_count}/{len(products)}")
    print(f"   - Unmatched: {unmatched_count}/{len(products)}")
    
    if unmatched_count > 0:
        print(f"\n⚠️  Cảnh báo: {unmatched_count} sản phẩm không có link affiliate")
    
    return products


if __name__ == "__main__":
    # Test module
    test_products = [
        {
            'original_link': 'https://shopee.vn/product/123/456',
            'name': 'Test Product',
            'url': 'https://s.shopee.vn/old_link'
        }
    ]
    
    # Tạo file CSV test
    test_csv = 'data/test_converted.csv'
    os.makedirs('data', exist_ok=True)
    
    with open(test_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Link Gốc', 'Link Affiliate'])
        writer.writerow(['https://shopee.vn/product/123/456', 'https://s.shopee.vn/NEW_LINK'])
    
    try:
        merged = merge_affiliate_links(test_products, test_csv)
        print(f"\n✅ Test thành công!")
        print(f"Link mới: {merged[0]['url']}")
    except Exception as e:
        print(f"❌ Test thất bại: {e}")
    finally:
        if os.path.exists(test_csv):
            os.remove(test_csv)
