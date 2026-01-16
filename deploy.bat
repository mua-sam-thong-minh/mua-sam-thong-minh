@echo off
REM Deploy script cho Windows

echo ========================================
echo   DEPLOY FLASHSALE PRODUCTS
echo ========================================
echo.

REM Kiểm tra xem file products.json có tồn tại không
if not exist "data\products.json" (
    echo [ERROR] File data\products.json khong ton tai!
    echo Vui long chay: python main.py --stage 3
    pause
    exit /b 1
)

echo [INFO] Dang commit va push len GitHub...
echo.

git add data\products.json
git commit -m "🔄 Update FlashSale products %date% %time%"
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   DEPLOY THANH CONG!
    echo ========================================
    echo.
    echo Website se cap nhat sau ~1 phut
) else (
    echo.
    echo [ERROR] Deploy that bai!
    echo Vui long kiem tra git status
)

pause
