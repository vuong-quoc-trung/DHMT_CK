import exifread
from PIL import Image
from transformers import pipeline
import matplotlib.pyplot as plt

def extract_exif(image_path):
    print("--- PHẦN 1: THÔNG SỐ KỸ THUẬT QUANG HỌC (EXIF) ---")
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f)
            
            # Lấy các thông số cơ bản
            focal_length = tags.get('EXIF FocalLength', 'Không tìm thấy')
            f_number = tags.get('EXIF FNumber', 'Không tìm thấy')
            width = tags.get('EXIF ExifImageWidth', 'Không tìm thấy')
            height = tags.get('EXIF ExifImageLength', 'Không tìm thấy')

            print(f"Tiêu cự (Focal Length) : {focal_length}")
            print(f"Khẩu độ (F-Number)     : {f_number}")
            print(f"Độ phân giải           : {width} x {height}")
            
    except Exception as e:
        print(f"Lỗi khi đọc file ảnh: {e}")

def estimate_depth(image_path):
    print("\n--- PHẦN 2: ƯỚC LƯỢNG CHIỀU SÂU BẰNG AI ---")
    print("Đang tải mô hình AI (Lần chạy đầu tiên sẽ mất vài phút để tải model)...")
    
    # Khởi tạo mô hình ước lượng chiều sâu (MiDaS)
    pipe = pipeline(task="depth-estimation")
    
    # Đọc ảnh
    img = Image.open(image_path)
    
    # Chạy mô hình để lấy kết quả
    print("Đang xử lý ảnh để tạo Depth Map...")
    result = pipe(img)
    depth_map = result["depth"]

    # Hiển thị trực quan kết quả
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    axes[0].imshow(img)
    axes[0].set_title("Ảnh Gốc (RGB)")
    axes[0].axis("off")

    axes[1].imshow(depth_map, cmap='inferno')
    axes[1].set_title("Bản đồ Chiều sâu (Depth Map)")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Đặt một bức ảnh vào cùng thư mục với file code và đổi tên thành 'test.jpg'
    IMAGE_FILE = 'test.jpg'
    
    extract_exif(IMAGE_FILE)
    estimate_depth(IMAGE_FILE)