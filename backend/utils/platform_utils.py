"""
平台工具：跨平台的鼠标位置和热键支持
"""
import platform
import sys

# 平台检测
IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'
IS_MAC = platform.system() == 'Darwin'

# 尝试导入库（优先pyautogui，因为它最可靠）
WIN32_AVAILABLE = False
PYAUTOGUI_AVAILABLE = False

# 优先尝试pyautogui（跨平台，最可靠）
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
    print("[平台工具] ✓ pyautogui 可用")
except ImportError:
    print("[平台工具] ✗ pyautogui 不可用，请安装: pip install pyautogui")

# Windows专用：win32api
if IS_WINDOWS:
    try:
        import win32api
        import win32con
        WIN32_AVAILABLE = True
        print("[平台工具] ✓ Windows: win32api 可用")
    except ImportError:
        print("[平台工具] ✗ Windows: win32api 不可用，请安装: pip install pywin32")


def get_mouse_position():
    """
    获取当前鼠标位置（跨平台）
    优先使用pyautogui，因为它最可靠
    返回: (x, y) 元组
    """
    # 优先使用pyautogui（最可靠）
    if PYAUTOGUI_AVAILABLE:
        try:
            import pyautogui
            pos = pyautogui.position()
            result = (int(pos.x), int(pos.y))
            print(f"[平台工具] pyautogui获取鼠标位置: {result}")
            return result
        except Exception as e:
            print(f"[平台工具] pyautogui获取鼠标位置失败: {e}")
            import traceback
            traceback.print_exc()
    
    # Windows备选：win32api
    if IS_WINDOWS and WIN32_AVAILABLE:
        try:
            import win32api
            pos = win32api.GetCursorPos()
            result = (int(pos[0]), int(pos[1]))
            print(f"[平台工具] win32api获取鼠标位置: {result}")
            return result
        except Exception as e:
            print(f"[平台工具] win32api获取鼠标位置失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 最后使用pynput（Linux/Mac或Windows备选）
    try:
        from pynput.mouse import Controller
        mouse_controller = Controller()
        pos = mouse_controller.position
        result = (int(pos[0]), int(pos[1]))
        print(f"[平台工具] pynput获取鼠标位置: {result}")
        return result
    except Exception as e:
        print(f"[平台工具] pynput获取鼠标位置失败: {e}")
        import traceback
        traceback.print_exc()
        return (0, 0)


def get_platform_info():
    """获取平台信息"""
    return {
        "platform": platform.system(),
        "win32_available": WIN32_AVAILABLE,
        "pyautogui_available": PYAUTOGUI_AVAILABLE,
        "is_windows": IS_WINDOWS,
        "is_linux": IS_LINUX,
        "is_mac": IS_MAC
    }

