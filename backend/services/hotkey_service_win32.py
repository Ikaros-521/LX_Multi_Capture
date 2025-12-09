"""
Windows专用热键服务（使用win32api）
"""
import threading
import ctypes
from ctypes import wintypes
from typing import Callable, Optional, Dict, Tuple
from backend.services.config_service import ConfigService

# Windows API常量
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

WM_HOTKEY = 0x0312

# VK代码映射
VK_CODE = {
    '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35,
    '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39, '0': 0x30,
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
    'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
    'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
    'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
    'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59,
    'z': 0x5A,
}


class HotkeyServiceWin32:
    """Windows专用热键服务（使用win32api）"""
    
    def __init__(self):
        self.config_service = ConfigService()
        self.hotkey_handlers: Dict[int, Callable] = {}
        self.is_listening = False
        self.listener_thread: Optional[threading.Thread] = None
        self.hotkey_id_counter = 1
        self.hotkey_id_map: Dict[str, int] = {}  # hotkey_str -> hotkey_id
        
        # 存储坐标采集的临时数据
        self.captured_coords: Dict[str, Optional[Tuple[int, int]]] = {
            'top_left': None,
            'bottom_right': None
        }
        
        # 创建隐藏窗口来接收热键消息
        self.hwnd = self._create_hidden_window()
        if not self.hwnd:
            print("[Win32热键] ⚠ 窗口创建失败，使用0（当前线程）")
            self.hwnd = None  # None表示使用0，RegisterHotKey会使用当前线程

    def _parse_hotkey(self, hotkey_str: str) -> tuple:
        """
        解析热键字符串
        返回: (modifiers, vk_code, hotkey_id)
        """
        parts = hotkey_str.lower().split('+')
        modifiers = 0
        vk_code = None
        
        for part in parts:
            part = part.strip()
            if part == 'ctrl' or part == 'control':
                modifiers |= MOD_CONTROL
            elif part == 'alt':
                modifiers |= MOD_ALT
            elif part == 'shift':
                modifiers |= MOD_SHIFT
            elif part == 'win' or part == 'cmd' or part == 'super':
                modifiers |= MOD_WIN
            elif len(part) == 1:
                vk_code = VK_CODE.get(part)
                if vk_code is None:
                    print(f"未知的虚拟键代码: {part}")
                    return None
            else:
                # 尝试作为数字
                if part.isdigit():
                    vk_code = VK_CODE.get(part)
                else:
                    print(f"无法解析热键部分: {part}")
                    return None
        
        if vk_code is None:
            print(f"热键缺少主键: {hotkey_str}")
            return None
        
        return (modifiers, vk_code)

    def register_hotkey(self, hotkey_str: str, callback: Callable) -> bool:
        """注册热键"""
        try:
            parsed = self._parse_hotkey(hotkey_str)
            if parsed is None:
                return False
            
            modifiers, vk_code = parsed
            hotkey_id = self.hotkey_id_counter
            self.hotkey_id_counter += 1
            
            # 注册系统热键（hwnd为None表示当前线程）
            result = ctypes.windll.user32.RegisterHotKey(
                self.hwnd if self.hwnd else 0,
                hotkey_id,
                modifiers,
                vk_code
            )
            
            if result:
                self.hotkey_handlers[hotkey_id] = callback
                self.hotkey_id_map[hotkey_str] = hotkey_id
                print(f"[Win32热键] 注册成功: {hotkey_str} -> ID={hotkey_id}, Mod={modifiers}, VK={vk_code}")
                return True
            else:
                error = ctypes.get_last_error()
                print(f"[Win32热键] 注册失败: {hotkey_str}, 错误代码: {error}")
                return False
        except Exception as e:
            print(f"[Win32热键] 注册异常: {hotkey_str}, {e}")
            import traceback
            traceback.print_exc()
            return False

    def unregister_hotkey(self, hotkey_str: str) -> bool:
        """注销热键"""
        if hotkey_str in self.hotkey_id_map:
            hotkey_id = self.hotkey_id_map[hotkey_str]
            ctypes.windll.user32.UnregisterHotKey(self.hwnd if self.hwnd else 0, hotkey_id)
            if hotkey_id in self.hotkey_handlers:
                del self.hotkey_handlers[hotkey_id]
            del self.hotkey_id_map[hotkey_str]
            return True
        return False

    def _message_loop(self):
        """Windows消息循环"""
        print(f"[Win32热键] 消息循环启动，HWND={self.hwnd}")
        print(f"[Win32热键] 已注册热键ID: {list(self.hotkey_handlers.keys())}")
        
        msg = wintypes.MSG()
        hwnd_param = self.hwnd if self.hwnd else None  # None表示接收所有消息
        
        while self.is_listening:
            try:
                # 使用PeekMessage非阻塞检查消息
                # 如果hwnd为None，接收所有窗口的消息（包括当前线程）
                bRet = ctypes.windll.user32.PeekMessageW(
                    ctypes.byref(msg), 
                    hwnd_param,  # 使用None接收所有消息
                    0, 
                    0, 
                    0x0001  # PM_REMOVE
                )
                
                if bRet:
                    # 有消息
                    if msg.message == WM_HOTKEY:
                        hotkey_id = msg.wParam
                        print(f"[Win32热键] ✓ 收到热键消息！ID={hotkey_id}")
                        print(f"[Win32热键] 可用处理器: {list(self.hotkey_handlers.keys())}")
                        if hotkey_id in self.hotkey_handlers:
                            try:
                                print(f"[Win32热键] 执行回调函数...")
                                self.hotkey_handlers[hotkey_id]()
                                print(f"[Win32热键] 回调执行完成")
                            except Exception as e:
                                print(f"[Win32热键] ✗ 回调执行错误: {e}")
                                import traceback
                                traceback.print_exc()
                        else:
                            print(f"[Win32热键] ⚠ 警告: 热键ID {hotkey_id} 没有对应的处理器")
                    
                    ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                    ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
                else:
                    # 没有消息，短暂休眠
                    import time
                    time.sleep(0.01)
            except Exception as e:
                print(f"[Win32热键] ✗ 消息循环错误: {e}")
                import traceback
                traceback.print_exc()
                import time
                time.sleep(0.1)
        
        print("[Win32热键] 消息循环结束")

    def start_listening(self):
        """开始监听热键"""
        if not self.is_listening:
            self.is_listening = True
            self.listener_thread = threading.Thread(target=self._message_loop, daemon=True)
            self.listener_thread.start()
            print("[Win32热键] 消息循环已启动")

    def stop_listening(self):
        """停止监听热键"""
        self.is_listening = False
        # 发送WM_QUIT消息
        try:
            ctypes.windll.user32.PostQuitMessage(0)
        except:
            pass

    def clear_captured_coords(self):
        """清除已采集的坐标"""
        self.captured_coords = {
            'top_left': None,
            'bottom_right': None
        }

    def get_captured_coords(self) -> Dict[str, Optional[Tuple[int, int]]]:
        """获取已采集的坐标"""
        return self.captured_coords.copy()

