"""
Fetcher Module - Thu thập dữ liệu từ dealhotday.com
"""
import requests
from fake_useragent import UserAgent
import time
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
REQUEST_DELAY = int(os.getenv('REQUEST_DELAY', 1))


def fetch_flashsale_data(date: str, time_slot: str) -> str:
    """
    Lấy dữ liệu FlashSale từ dealhotday.com
    
    Args:
        date: Định dạng DD.MM.YYYY (VD: "16.01.2026")
        time_slot: Khung giờ (VD: "17.00")
    
    Returns:
        HTML content chứa JSON nhúng
        
    Raises:
        requests.RequestException: Khi request thất bại sau MAX_RETRIES lần
    """
    url = f"https://dealhotday.com/FlashSale-Shopee/{date}-{time_slot}/all"
    ua = UserAgent()
    
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    last_error = None
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"🔄 Đang gửi request đến {url} (lần thử {attempt + 1}/{MAX_RETRIES})...")
            
            response = requests.get(
                url, 
                headers=headers, 
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            
            print(f"✅ Request thành công! Status: {response.status_code}")
            print(f"📦 Kích thước dữ liệu: {len(response.text):,} bytes")
            
            return response.text
            
        except requests.RequestException as e:
            last_error = e
            print(f"❌ Lần thử {attempt + 1} thất bại: {str(e)}")
            
            if attempt < MAX_RETRIES - 1:
                wait_time = REQUEST_DELAY * (attempt + 1)
                print(f"⏳ Chờ {wait_time}s trước khi thử lại...")
                time.sleep(wait_time)
    
    # Nếu tất cả các lần thử đều thất bại
    raise requests.RequestException(
        f"Không thể lấy dữ liệu sau {MAX_RETRIES} lần thử. Lỗi cuối: {last_error}"
    )


def fetch_current_flashsale() -> str:
    """
    Lấy dữ liệu FlashSale của ngày hiện tại
    Tự động xác định khung giờ gần nhất
    
    Returns:
        HTML content
    """
    from datetime import datetime
    
    now = datetime.now()
    date_str = now.strftime("%d.%m.%Y")
    
    # Xác định khung giờ (Shopee thường có: 00.00, 09.00, 12.00, 17.00, 20.00, 22.00)
    hour = now.hour
    time_slots = ["00.00", "09.00", "12.00", "17.00", "20.00", "22.00"]
    
    # Tìm khung giờ gần nhất
    time_slot = "17.00"  # Default
    for slot in time_slots:
        slot_hour = int(slot.split('.')[0])
        if hour >= slot_hour:
            time_slot = slot
    
    print(f"📅 Ngày: {date_str}")
    print(f"⏰ Khung giờ: {time_slot}")
    
    return fetch_flashsale_data(date_str, time_slot)


if __name__ == "__main__":
    # Test module
    try:
        html = fetch_current_flashsale()
        print(f"\n✅ Thành công! Lấy được {len(html):,} bytes dữ liệu")
        
        # Kiểm tra xem có chứa ITEMS không
        if "const ITEMS = [" in html:
            print("✅ Phát hiện dữ liệu ITEMS trong HTML")
        else:
            print("⚠️  Không tìm thấy dữ liệu ITEMS")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
