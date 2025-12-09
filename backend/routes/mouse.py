"""
鼠标位置路由（用于交互式选区设置）
"""
from fastapi import APIRouter
from backend.models import MousePosition

router = APIRouter(prefix="/api/mouse", tags=["mouse"])

# 延迟导入避免循环依赖，使用全局实例
_hotkey_service = None

def get_hotkey_service():
    """获取热键服务实例（使用main.py中的全局实例）"""
    global _hotkey_service
    if _hotkey_service is None:
        # 从main模块导入全局实例
        import backend.main as main_module
        _hotkey_service = main_module.hotkey_service
    return _hotkey_service


@router.get("/position", response_model=MousePosition)
async def get_mouse_position():
    """获取当前鼠标位置（跨平台）"""
    from backend.utils.platform_utils import get_mouse_position
    pos = get_mouse_position()
    return MousePosition(x=pos[0], y=pos[1])


@router.get("/captured-coords")
async def get_captured_coords():
    """获取通过热键采集的坐标"""
    hotkey_service = get_hotkey_service()
    coords = hotkey_service.get_captured_coords()
    # 确保返回格式正确
    result = {
        "top_left": coords.get('top_left'),
        "bottom_right": coords.get('bottom_right')
    }
    # 调试信息
    print(f"[API] /captured-coords 被调用，返回: {result}")
    return result


@router.post("/clear-coords")
async def clear_captured_coords():
    """清除已采集的坐标"""
    hotkey_service = get_hotkey_service()
    hotkey_service.clear_captured_coords()
    return {"message": "坐标已清除"}


@router.get("/test-hotkey")
async def test_hotkey():
    """测试热键服务状态"""
    hotkey_service = get_hotkey_service()
    config = hotkey_service.config_service.get_config()
    
    # 获取平台信息
    from backend.utils.platform_utils import get_platform_info
    platform_info = get_platform_info()
    
    result = {
        "is_listening": hotkey_service.is_listening,
        "platform_info": platform_info,
        "config": {
            "hotkey_a": config.hotkey_a,
            "hotkey_b": config.hotkey_b,
            "hotkey_c": config.hotkey_c
        },
        "current_coords": hotkey_service.get_captured_coords()
    }
    
    # 添加注册的热键信息
    if hasattr(hotkey_service, 'hotkeys'):
        result["registered_hotkeys"] = list(hotkey_service.hotkeys.keys())
    if hasattr(hotkey_service, 'win32_service') and hotkey_service.win32_service:
        result["hotkey_implementation"] = "win32"
        if hasattr(hotkey_service.win32_service, 'hotkey_id_map'):
            result["registered_hotkeys"] = list(hotkey_service.win32_service.hotkey_id_map.keys())
    else:
        result["hotkey_implementation"] = "pynput"
    
    return result

