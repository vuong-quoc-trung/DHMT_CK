"""
Main GUI - Giao diện chính của ứng dụng Xử lý Ảnh AI.
Đóng vai trò tầng Presentation (View/Controller) trong kiến trúc phân tầng.

Chạy chương trình: python main_gui.py
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# Thêm thư mục gốc vào sys.path để import các module
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from services.exif_service import get_exif_data
from services.ai_service import DepthEstimator
from repositories.file_storage import save_history


class AppGUI:
    """
    Class giao diện người dùng chính sử dụng tkinter.
    Kích thước cửa sổ: 550x450 (Đã tăng chiều cao để chứa đủ chữ).
    """

    def __init__(self):
        """Khởi tạo cửa sổ và các thành phần giao diện."""
        self.root = tk.Tk()
        self.root.title("Ứng dụng Xử lý Ảnh AI - Depth Estimation")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        # Biến trạng thái
        self.image_path = None
        self.exif_data = None
        self.depth_estimator = None  # Lazy initialization - chỉ khởi tạo khi cần

        # Xây dựng giao diện
        self._build_ui()

    def _build_ui(self):
        """Xây dựng toàn bộ các UI component."""

        # ===== TIÊU ĐỀ =====
        label_title = tk.Label(
            self.root,
            text="🖼️ Ứng dụng Xử lý Ảnh AI",
            font=("Arial", 18, "bold"),
            fg="#2c3e50",
            pady=10
        )
        label_title.pack()

        label_subtitle = tk.Label(
            self.root,
            text="Depth Map Estimation & EXIF Reader",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        label_subtitle.pack()

        # ===== SEPARATOR =====
        separator1 = tk.Frame(self.root, height=2, bg="#bdc3c7")
        separator1.pack(fill=tk.X, padx=20, pady=10)

        # ===== NÚT CHỌN ẢNH =====
        self.btn_select = tk.Button(
            self.root,
            text="1. Chọn ảnh đầu vào",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5,
            command=self._on_select_image
        )
        self.btn_select.pack(pady=5)

        # ===== LABEL ĐƯỜNG DẪN ẢNH =====
        self.label_path = tk.Label(
            self.root,
            text="Chưa chọn ảnh",
            font=("Arial", 9),
            fg="#95a5a6",
            wraplength=500
        )
        self.label_path.pack(pady=3)

        # ===== SEPARATOR =====
        separator2 = tk.Frame(self.root, height=1, bg="#ecf0f1")
        separator2.pack(fill=tk.X, padx=30, pady=5)

        # ===== LABEL THÔNG TIN EXIF =====
        label_exif_title = tk.Label(
            self.root,
            text="📋 Thông tin EXIF:",
            font=("Arial", 11, "bold"),
            fg="#2c3e50",
            anchor="w"
        )
        label_exif_title.pack(padx=30, anchor="w")

        self.label_exif = tk.Label(
            self.root,
            text="(Chưa có dữ liệu - Hãy chọn ảnh trước)",
            font=("Consolas", 10),
            fg="#7f8c8d",
            justify=tk.LEFT,
            anchor="w",
            wraplength=480
        )
        self.label_exif.pack(padx=40, anchor="w", pady=5)

        # ===== SEPARATOR =====
        separator3 = tk.Frame(self.root, height=2, bg="#bdc3c7")
        separator3.pack(fill=tk.X, padx=20, pady=10)

        # ===== NÚT TÁI TẠO DEPTH MAP =====
        self.btn_process = tk.Button(
            self.root,
            text="2. Tái tạo Depth Map & Lưu File",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5,
            command=self._on_process
        )
        self.btn_process.pack(pady=10)

        # ===== LABEL TRẠNG THÁI =====
        self.label_status = tk.Label(
            self.root,
            text="",
            font=("Arial", 9),
            fg="#e74c3c"
        )
        self.label_status.pack(pady=3)

    def _on_select_image(self):
        """Xử lý sự kiện khi người dùng bấm nút Chọn ảnh."""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh đầu vào",
            initialdir=os.path.join(BASE_DIR, "input_images"),
            filetypes=[
                ("Ảnh", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("Tất cả", "*.*")
            ]
        )

        if not file_path:
            return  # Người dùng bấm Cancel

        self.image_path = file_path
        self.label_path.config(text=f"📁 {file_path}", fg="#2c3e50")

        # Đọc thông tin EXIF
        self.exif_data = get_exif_data(file_path)

        if self.exif_data:
            exif_text = (
                f"• Máy ảnh (Camera):       {self.exif_data.get('CameraModel', 'N/A')}\n"
                f"• ISO:                    {self.exif_data.get('ISO', 'N/A')}\n"
                f"• Tốc độ chụp (Exposure): {self.exif_data.get('ExposureTime', 'N/A')}s\n"
                f"• Tiêu cự (Focal Length): {self.exif_data.get('FocalLength', 'N/A')}\n"
                f"• Khẩu độ (F-Number):     {self.exif_data.get('FNumber', 'N/A')}\n"
                f"• Độ phân giải gốc:       {self.exif_data.get('Width', 'N/A')} x {self.exif_data.get('Height', 'N/A')} px"
            )
            self.label_exif.config(text=exif_text, fg="#2c3e50")
        else:
            self.label_exif.config(
                text="⚠️ Không tìm thấy dữ liệu EXIF trong ảnh này.",
                fg="#e67e22"
            )

        self.label_status.config(text="✅ Đã chọn ảnh thành công!", fg="#27ae60")

    def _on_process(self):
        """Xử lý sự kiện khi người dùng bấm nút Tái tạo Depth Map."""
        if not self.image_path:
            messagebox.showwarning(
                "Cảnh báo",
                "Vui lòng chọn ảnh đầu vào trước!"
            )
            return

        # Disable nút bấm và đổi text
        self.btn_process.config(
            text="⏳ Đang xử lý...",
            state=tk.DISABLED,
            bg="#95a5a6"
        )
        self.btn_select.config(state=tk.DISABLED)
        self.label_status.config(text="⏳ Đang xử lý AI, vui lòng chờ...", fg="#e67e22")
        self.root.update_idletasks()

        # Chạy xử lý trong thread riêng để không đóng băng GUI
        thread = threading.Thread(target=self._run_processing, daemon=True)
        thread.start()

    def _run_processing(self):
        """Thực hiện xử lý AI trong background thread."""
        try:
            # Khởi tạo DepthEstimator nếu chưa có (lazy init)
            if self.depth_estimator is None:
                self.root.after(0, lambda: self.label_status.config(
                    text="⏳ Đang tải mô hình AI lần đầu...", fg="#e67e22"
                ))
                self.depth_estimator = DepthEstimator()

            # Tạo tên file output
            image_name = os.path.splitext(os.path.basename(self.image_path))[0]
            output_filename = f"depth_{image_name}.png"

            # Chạy AI tạo Depth Map
            output_path = self.depth_estimator.generate_depth_map(
                self.image_path, output_filename
            )

            if output_path is None:
                self.root.after(0, lambda: self._show_error(
                    "Lỗi khi tạo Depth Map. Vui lòng kiểm tra console."
                ))
                return

            # Lưu lịch sử vào CSV
            save_history(self.image_path, self.exif_data, output_path)

            # Hiển thị thông báo thành công (phải chạy trên main thread)
            self.root.after(0, lambda: self._show_success(output_path))

        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self._show_error(error_msg))

    def _show_success(self, output_path):
        """Hiển thị thông báo thành công và khôi phục nút bấm."""
        messagebox.showinfo(
            "Thành công! ✅",
            f"Đã tạo Depth Map thành công!\n\n"
            f"📁 File kết quả:\n{output_path}\n\n"
            f"📋 Lịch sử đã được lưu vào history_log.csv"
        )
        self._restore_buttons()
        self.label_status.config(text="✅ Xử lý hoàn tất!", fg="#27ae60")

    def _show_error(self, error_msg):
        """Hiển thị thông báo lỗi và khôi phục nút bấm."""
        messagebox.showerror(
            "Lỗi ❌",
            f"Đã xảy ra lỗi:\n{error_msg}"
        )
        self._restore_buttons()
        self.label_status.config(text="❌ Xử lý thất bại!", fg="#e74c3c")

    def _restore_buttons(self):
        """Khôi phục trạng thái ban đầu cho các nút bấm."""
        self.btn_process.config(
            text="2. Tái tạo Depth Map & Lưu File",
            state=tk.NORMAL,
            bg="#27ae60"
        )
        self.btn_select.config(state=tk.NORMAL)

    def run(self):
        """Chạy vòng lặp chính của ứng dụng."""
        self.root.mainloop()

# ===== ENTRY POINT =====
if __name__ == "__main__":
    app = AppGUI()
    app.run()