"""
File Storage Repository - Lưu trữ lịch sử xử lý ảnh vào file CSV.
Thuộc tầng Repository (Data Access) trong kiến trúc phân tầng (Layered Architecture).
"""

import os
import csv
from datetime import datetime

# Đường dẫn file CSV lưu lịch sử
HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'history_log.csv')

# Header cho file CSV (Đã cập nhật thêm 3 cột mới)
CSV_HEADER = ['Thời gian', 'Tên ảnh', 'Máy ảnh', 'ISO', 'Tốc độ chụp', 'Tiêu cự', 'Khẩu độ', 'Độ phân giải', 'File xuất ra']

def save_history(image_path, exif_data, output_path):
    """
    Lưu một bản ghi lịch sử xử lý ảnh vào file CSV.
    Nếu file CSV chưa tồn tại, tự động tạo mới kèm dòng Header.
    """
    try:
        # Đảm bảo thư mục output tồn tại
        output_dir = os.path.dirname(HISTORY_FILE)
        os.makedirs(output_dir, exist_ok=True)

        # Kiểm tra file đã tồn tại chưa
        file_exists = os.path.isfile(HISTORY_FILE)

        # Chuẩn bị dữ liệu
        ten_anh = os.path.basename(image_path)
        thoi_gian = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if exif_data:
            may_anh = exif_data.get('CameraModel', 'N/A')
            iso = exif_data.get('ISO', 'N/A')
            toc_do = exif_data.get('ExposureTime', 'N/A')
            tieu_cu = exif_data.get('FocalLength', 'N/A')
            khau_do = exif_data.get('FNumber', 'N/A')
            width = exif_data.get('Width', 'N/A')
            height = exif_data.get('Height', 'N/A')
            do_phan_giai = f"{width} x {height}"
        else:
            may_anh = iso = toc_do = tieu_cu = khau_do = do_phan_giai = 'N/A'

        file_xuat = os.path.basename(output_path) if output_path else 'N/A'

        # Ghi vào file CSV
        with open(HISTORY_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Ghi header nếu file mới tạo
            if not file_exists:
                writer.writerow(CSV_HEADER)

            # Ghi dòng dữ liệu full 9 cột
            writer.writerow([thoi_gian, ten_anh, may_anh, iso, toc_do, tieu_cu, khau_do, do_phan_giai, file_xuat])

        print(f"[Repository] Đã lưu lịch sử xử lý ảnh '{ten_anh}' vào {HISTORY_FILE}")

    except PermissionError:
        print(f"[Repository] Lỗi: Không có quyền ghi vào file '{HISTORY_FILE}'.")
    except Exception as e:
        print(f"[Repository] Lỗi khi lưu lịch sử: {e}")