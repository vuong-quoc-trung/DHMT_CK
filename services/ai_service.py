"""
AI Service - Ước lượng Depth Map bằng mô hình AI (Transformers).
Thuộc tầng Service trong kiến trúc phân tầng (Layered Architecture).
"""

import os
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Sử dụng backend không cần GUI cho matplotlib
import matplotlib.pyplot as plt
from transformers import pipeline


class DepthEstimator:
    """
    Class thực hiện ước lượng bản đồ độ sâu (Depth Map) từ ảnh đầu vào
    sử dụng pipeline depth-estimation của Hugging Face Transformers.
    """

    def __init__(self):
        """
        Khởi tạo pipeline depth-estimation.
        Model mặc định sẽ được tải về tự động từ Hugging Face Hub.
        """
        print("[AI Service] Đang tải mô hình Depth Estimation... (lần đầu sẽ mất vài phút)")
        self.pipe = pipeline(task="depth-estimation")
        print("[AI Service] Tải mô hình thành công!")

    def generate_depth_map(self, image_path, output_filename):
        """
        Tạo bản đồ độ sâu từ ảnh đầu vào và lưu kết quả so sánh.

        Args:
            image_path (str): Đường dẫn tuyệt đối đến file ảnh gốc.
            output_filename (str): Tên file kết quả sẽ lưu vào thư mục output/.

        Returns:
            str: Đường dẫn tuyệt đối đến file kết quả đã lưu.
                 Trả về None nếu xảy ra lỗi.
        """
        try:
            # Đọc ảnh gốc
            img = Image.open(image_path).convert("RGB")

            # Chạy pipeline depth-estimation
            print("[AI Service] Đang xử lý Depth Estimation...")
            result = self.pipe(img)
            depth_map = result["depth"]

            # Tạo figure so sánh: Ảnh gốc | Depth Map
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))

            # Cột 1: Ảnh gốc
            axes[0].imshow(img)
            axes[0].set_title("Ảnh gốc", fontsize=14, fontweight='bold')
            axes[0].axis('off')

            # Cột 2: Depth Map
            axes[1].imshow(depth_map, cmap='inferno')
            axes[1].set_title("Depth Map", fontsize=14, fontweight='bold')
            axes[1].axis('off')

            plt.tight_layout()

            # Xác định đường dẫn lưu file
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, output_filename)

            # Lưu figure
            fig.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close(fig)

            print(f"[AI Service] Đã lưu kết quả tại: {output_path}")
            return output_path

        except FileNotFoundError:
            print(f"[AI Service] Lỗi: Không tìm thấy file ảnh '{image_path}'.")
            return None
        except Exception as e:
            print(f"[AI Service] Lỗi khi tạo Depth Map: {e}")
            return None
