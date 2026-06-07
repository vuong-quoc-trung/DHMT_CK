"""
EXIF Service - Trích xuất thông tin EXIF từ ảnh.
Thuộc tầng Service trong kiến trúc phân tầng (Layered Architecture).
"""
import exifread
from PIL import Image

def get_exif_data(image_path):
    try:
        # Dùng Pillow (Image) để lấy chiều rộng/cao 100% thành công
        with Image.open(image_path) as img:
            width, height = img.size

        # Đọc các thông số quang học sâu bằng exifread
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)

        # Trả về bộ dữ liệu xịn sò hơn
        return {
            'CameraModel': str(tags.get('Image Model', 'N/A')),
            'ISO': str(tags.get('EXIF ISOSpeedRatings', 'N/A')),
            'ExposureTime': str(tags.get('EXIF ExposureTime', 'N/A')),
            'FocalLength': str(tags.get('EXIF FocalLength', 'N/A')),
            'FNumber': str(tags.get('EXIF FNumber', 'N/A')),
            'Width': str(width),
            'Height': str(height)
        }
    except Exception as e:
        print(f"[EXIF Service] Lỗi khi đọc EXIF: {e}")
        return None