"""
Main Entry Point - Hệ thống Thu thập & Chuyển đổi Link Affiliate Shopee
"""
import argparse
import sys
import os
from datetime import datetime

# Fix encoding cho Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Import các module
from src.fetcher import fetch_flashsale_data, fetch_current_flashsale
from src.parser import extract_products_from_html, get_statistics
from src.link_builder import build_links_for_products
from src.exporter import export_links_to_csv, export_simple_links_xlsx
from src.merger import merge_affiliate_links
from src.json_generator import generate_products_only_json, validate_json_output


def print_banner():
    """In banner chào mừng"""
    print("=" * 70)
    print("HE THONG THU THAP & CHUYEN DOI LINK AFFILIATE SHOPEE")
    print("=" * 70)
    print()


def stage_1_collect(date: str = None, time_slot: str = None):
    """
    GIAI ĐOẠN 1: Thu thập & Sơ chế dữ liệu
    
    Args:
        date: Ngày (DD.MM.YYYY), None = hôm nay
        time_slot: Khung giờ (HH.MM), None = auto detect
    """
    print("\n" + "=" * 70)
    print("📥 GIAI ĐOẠN 1: THU THẬP & SƠ CHẾ DỮ LIỆU")
    print("=" * 70 + "\n")
    
    try:
        # Bước 1: Fetch HTML
        if date and time_slot:
            html = fetch_flashsale_data(date, time_slot)
        else:
            html = fetch_current_flashsale()
        
        # Bước 2: Parse JSON
        products = extract_products_from_html(html)
        
        # Bước 3: Tái tạo link gốc
        products = build_links_for_products(products)
        
        # Bước 4: Xuất CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSV chi tiết
        detailed_csv = f"data/input_links_{timestamp}.csv"
        export_links_to_csv(products, detailed_csv)
        
        # Excel đơn giản (để upload lên Shopee)
        simple_xlsx = f"data/input_links_simple_{timestamp}.xlsx"
        export_simple_links_xlsx(products, simple_xlsx)
        
        # Lưu dữ liệu tạm để dùng cho stage 2
        import json
        temp_file = "data/temp_products.json"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        # Thống kê
        stats = get_statistics(products)
        print("\n" + "=" * 70)
        print("📊 THỐNG KÊ")
        print("=" * 70)
        print(f"Tổng số sản phẩm: {stats.get('total', 0)}")
        print(f"Shop Mall: {stats.get('mall', 0)}")
        print(f"Shop Yêu thích: {stats.get('preferred', 0)}")
        print(f"Giảm giá trung bình: {stats.get('avg_discount', 0):.1f}%")
        print(f"Giá trung bình: {stats.get('avg_price', 0):,.0f} VNĐ")
        
        print("\n" + "=" * 70)
        print("✅ GIAI ĐOẠN 1 HOÀN TẤT!")
        print("=" * 70)
        print(f"\n📁 File CSV chi tiết: {detailed_csv}")
        print(f"📁 File Excel đơn giản: {simple_xlsx}")
        print("\n📌 BƯỚC TIẾP THEO:")
        print("   1. Mở file Excel đơn giản (.xlsx)")
        print("   2. Upload lên Shopee Affiliate Portal để convert")
        print("   3. Tải file kết quả về và lưu vào: data/converted_links.csv")
        print("   4. Chạy: python main.py --stage 2")
        
        return True
        
    except Exception as e:
        print(f"\n❌ LỖI GIAI ĐOẠN 1: {e}")
        import traceback
        traceback.print_exc()
        return False


def stage_2_merge():
    """
    GIAI ĐOẠN 2: Merge link affiliate
    """
    print("\n" + "=" * 70)
    print("🔗 GIAI ĐOẠN 2: CHUYỂN ĐỔI LINK AFFILIATE")
    print("=" * 70 + "\n")
    
    try:
        # Đọc dữ liệu tạm từ stage 1
        import json
        temp_file = "data/temp_products.json"
        
        if not os.path.exists(temp_file):
            raise FileNotFoundError(
                "Không tìm thấy dữ liệu từ Giai đoạn 1. "
                "Vui lòng chạy: python main.py --stage 1"
            )
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        print(f"✅ Đã load {len(products)} sản phẩm từ Giai đoạn 1")
        
        # Merge với converted links
        converted_csv = "data/converted_links.csv"
        products = merge_affiliate_links(products, converted_csv)
        
        # Lưu lại để dùng cho stage 3
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 70)
        print("✅ GIAI ĐOẠN 2 HOÀN TẤT!")
        print("=" * 70)
        print("\n📌 BƯỚC TIẾP THEO:")
        print("   Chạy: python main.py --stage 3")
        
        return True
        
    except Exception as e:
        print(f"\n❌ LỖI GIAI ĐOẠN 2: {e}")
        import traceback
        traceback.print_exc()
        return False


def stage_3_export():
    """
    GIAI ĐOẠN 3: Xuất JSON và deploy
    """
    print("\n" + "=" * 70)
    print("📦 GIAI ĐOẠN 3: ĐÓNG GÓI & TRIỂN KHAI")
    print("=" * 70 + "\n")
    
    try:
        # Đọc dữ liệu từ stage 2
        import json
        temp_file = "data/temp_products.json"
        
        if not os.path.exists(temp_file):
            raise FileNotFoundError(
                "Không tìm thấy dữ liệu từ Giai đoạn 2. "
                "Vui lòng chạy: python main.py --stage 2"
            )
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        # Xuất JSON cuối cùng
        output_json = "data/products.json"
        generate_products_only_json(products, output_json)
        
        # Validate
        if validate_json_output(output_json):
            print("\n✅ Validation thành công!")
        
        print("\n" + "=" * 70)
        print("✅ GIAI ĐOẠN 3 HOÀN TẤT!")
        print("=" * 70)
        print(f"\n📁 File JSON cuối cùng: {output_json}")
        print("\n📌 BƯỚC TIẾP THEO:")
        print("   1. Commit và push file lên GitHub:")
        print("      git add data/products.json")
        print("      git commit -m '🔄 Update FlashSale products'")
        print("      git push")
        print("   2. Website sẽ tự động cập nhật sau ~1 phút")
        
        # Cleanup temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print("\n🧹 Đã dọn dẹp file tạm")
        
        return True
        
    except Exception as e:
        print(f"\n❌ LỖI GIAI ĐOẠN 3: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Hệ thống thu thập & chuyển đổi link affiliate Shopee'
    )
    parser.add_argument(
        '--stage',
        type=int,
        choices=[1, 2, 3],
        help='Giai đoạn cần chạy (1: Thu thập, 2: Merge, 3: Export)'
    )
    parser.add_argument(
        '--date',
        type=str,
        help='Ngày (DD.MM.YYYY), mặc định: hôm nay'
    )
    parser.add_argument(
        '--time',
        type=str,
        help='Khung giờ (HH.MM), mặc định: auto detect'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Chạy tất cả 3 giai đoạn (yêu cầu converted_links.csv đã sẵn sàng)'
    )
    
    args = parser.parse_args()
    
    # Nếu không có argument, hiển thị help
    if not any([args.stage, args.all]):
        parser.print_help()
        print("\n💡 VÍ DỤ SỬ DỤNG:")
        print("   python main.py --stage 1                    # Chạy Giai đoạn 1")
        print("   python main.py --stage 1 --date 16.01.2026 --time 17.00")
        print("   python main.py --stage 2                    # Chạy Giai đoạn 2")
        print("   python main.py --stage 3                    # Chạy Giai đoạn 3")
        return
    
    # Chạy theo stage
    if args.all:
        print("⚠️  Chế độ --all yêu cầu file converted_links.csv đã sẵn sàng!")
        success = stage_1_collect(args.date, args.time)
        if success:
            input("\n⏸️  Nhấn Enter sau khi đã upload converted_links.csv...")
            success = stage_2_merge()
            if success:
                stage_3_export()
    elif args.stage == 1:
        stage_1_collect(args.date, args.time)
    elif args.stage == 2:
        stage_2_merge()
    elif args.stage == 3:
        stage_3_export()


if __name__ == "__main__":
    main()
