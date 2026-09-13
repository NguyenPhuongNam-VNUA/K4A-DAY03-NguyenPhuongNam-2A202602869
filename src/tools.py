"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND (SUPPLY CHAIN & WAREHOUSE)
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
Chủ đề: Trợ lý Đơn hàng & Kho vận (Supply Chain Agent)
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu đơn hàng và vị trí kho
    {
        "name": "order_query",
        "description": "Tra cứu thông tin chi tiết đơn hàng, vị trí lưu kho, sản phẩm và trạng thái vận đơn bằng mã vận đơn.",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_id": {
                    "type": "string",
                    "description": "Mã vận đơn cần tra cứu (ví dụ: 'VN2026_001', 'VN2026_002')"
                }
            },
            "required": ["tracking_id"]
        }
    },
    
    # Tool 2: Cập nhật trạng thái đơn hàng và vị trí kho
    {
        "name": "update_order_status",
        "description": "Cập nhật trạng thái đơn hàng và vị trí kho vận (ví dụ: 'Đang xuất kho', 'Đang giao hàng', 'Đã giao hàng').",
        "parameters": {
            "type": "object",
            "properties": {
                "tracking_id": {
                    "type": "string",
                    "description": "Mã vận đơn cần cập nhật (ví dụ: 'VN2026_001')"
                },
                "new_status": {
                    "type": "string",
                    "description": "Trạng thái mới của đơn hàng (ví dụ: 'Đang xuất kho', 'Đang giao hàng', 'Đã giao hàng')"
                },
                "warehouse_location": {
                    "type": "string",
                    "description": "Vị trí kho hoặc địa điểm cập nhật (ví dụ: 'Kho Tổng Hà Nội - Kệ B3', 'Kho Tân Bình - TP.HCM')"
                }
            },
            "required": ["tracking_id", "new_status"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "VN2026_001": {
        "item_name": "iPhone 16 Pro Max 256GB",
        "quantity": 1,
        "recipient_name": "Nguyễn Văn An",
        "recipient_phone": "0987654321",
        "warehouse_location": "Kho Tổng Hà Nội - Kệ B3",
        "status": "Lưu kho",
        "carrier": "Viettel Post",
        "created_date": "10/09/2026"
    },
    "VN2026_002": {
        "item_name": "Laptop Dell XPS 15",
        "quantity": 2,
        "recipient_name": "Trần Thị Bình",
        "recipient_phone": "0912345678",
        "warehouse_location": "Kho Tân Bình - TP.HCM - Kệ A1",
        "status": "Đang giao hàng",
        "carrier": "VNPost",
        "created_date": "11/09/2026"
    }
}


def execute_order_query(tracking_id: str) -> str:
    """Thực thi tra cứu thông tin vận đơn và vị trí kho theo mã vận đơn"""
    key = tracking_id.strip().upper()

    # ở đây dùng get(key) không dùng MOCK_DATABASE[key] tránh lỗi key
    # không tồn tại sẽ bị lỗi KeyError gây sập toàn bộ chương trình
    order = MOCK_DATABASE.get(key)
    if order:

        # ensure_ascii=False để đảm bảo tiếng việt hiển thị được
        # mặc định Python biến thành mã UNICODE \u0110ang giao
        return json.dumps({
            "status": "SUCCESS",
            "tracking_id": key,
            "data": order
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu vận đơn có mã '{tracking_id}' trong hệ thống kho vận."
        }, ensure_ascii=False)


def execute_update_order_status(tracking_id: str, new_status: str, warehouse_location: str = "Kho Tổng Hà Nội - Kệ B3") -> str:
    """Thực thi cập nhật trạng thái đơn hàng và vị trí lưu kho"""
    key = tracking_id.strip().upper()
    if key in MOCK_DATABASE:
        MOCK_DATABASE[key]["status"] = new_status
        if warehouse_location:
            MOCK_DATABASE[key]["warehouse_location"] = warehouse_location
        return json.dumps({
            "status": "SUCCESS",
            "update_id": f"UP-{key}-2026",
            "tracking_id": key,
            "new_status": new_status,
            "warehouse_location": warehouse_location,
            "message": f"Cập nhật thành công: Đơn hàng {key} đã chuyển sang trạng thái '{new_status}' tại '{warehouse_location}'."
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không thể cập nhật. Không tìm thấy mã vận đơn '{tracking_id}' trong hệ thống."
        }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "order_query": execute_order_query,
    "update_order_status": execute_update_order_status
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)
