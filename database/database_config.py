# database/database_config.py
import os

# Sử dụng biến môi trường cho cấu hình là tốt nhất,
# nhưng để giữ nguyên yêu cầu ban đầu của bạn, tôi sẽ định nghĩa trực tiếp.
# Bạn có thể dễ dàng thay đổi để đọc từ biến môi trường sau này.

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '246357'), # Cân nhắc không hardcode password
    'database': os.getenv('DB_NAME', 'diabetesDB'),
}

# Bạn có thể thêm các cấu hình khác vào đây trong tương lai nếu cần
# VÍ DỤ:
# API_KEYS = {
# 'some_service': 'your_api_key_here'
# }
# DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'