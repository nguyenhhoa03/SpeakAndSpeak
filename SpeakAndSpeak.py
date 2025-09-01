#!/usr/bin/env python3
import os
import sys
import platform
import subprocess

def get_app_path():
    """Lấy đường dẫn đến file app.py trong thư mục app"""
    # Lấy thư mục chứa script hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Tạo đường dẫn đến app/app.py
    app_path = os.path.join(current_dir, "app", "app.py")
    return app_path

def run_app():
    """Chạy app.py dựa trên hệ điều hành"""
    app_path = get_app_path()
    
    # Kiểm tra xem file app.py có tồn tại không
    if not os.path.exists(app_path):
        print(f"Lỗi: Không tìm thấy file {app_path}")
        sys.exit(1)
    
    # Xác định hệ điều hành
    os_name = platform.system().lower()
    
    try:
        if os_name == "windows":
            # Windows: dùng pythonw để chạy trong nền và thoát terminal
            print("Đang khởi chạy ứng dụng trên Windows...")
            subprocess.Popen([
                "pythonw", app_path
            ], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            print("Ứng dụng đã được khởi chạy. Terminal sẽ đóng.")
            
        elif os_name in ["linux", "darwin"]:  # darwin là macOS
            # Linux và macOS: chạy bình thường
            system_name = "macOS" if os_name == "darwin" else "Linux"
            print(f"Đang khởi chạy ứng dụng trên {system_name}...")
            subprocess.run([sys.executable, app_path])
            
        else:
            print(f"Hệ điều hành '{os_name}' không được hỗ trợ")
            sys.exit(1)
            
    except FileNotFoundError as e:
        if os_name == "windows" and "pythonw" in str(e):
            print("Lỗi: Không tìm thấy pythonw. Đang thử dùng python thay thế...")
            try:
                subprocess.Popen([
                    "python", app_path
                ], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                print("Ứng dụng đã được khởi chạy bằng python.")
            except Exception as fallback_error:
                print(f"Lỗi khi chạy ứng dụng: {fallback_error}")
                sys.exit(1)
        else:
            print(f"Lỗi khi chạy ứng dụng: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_app()