"""
热键服务：负责全局热键的注册和监听（跨平台）
优先使用keyboard库（更可靠），备选pynput
"""
import platform
import threading
from typing import Callable, Optional, Dict, Tuple
from backend.services.config_service import ConfigService

IS_WINDOWS = platform.system() == 'Windows'

# 尝试导入keyboard库（更可靠）
KEYBOARD_AVAILABLE = False
kb_lib = None
keyboard = None

try:
    import keyboard as kb_lib
    KEYBOARD_AVAILABLE = True
    print("[热键服务] ✓ keyboard库可用（推荐）")
except ImportError:
    print("[热键服务] keyboard库不可用，使用pynput")
    try:
        from pynput import keyboard
    except ImportError:
        print("[热键服务] ✗ pynput也不可用！")


class HotkeyService:
    """热键服务（跨平台）"""
    
    def __init__(self):
        self.config_service = ConfigService()
        self.hotkey_handlers: Dict[str, Callable] = {}
        self.is_listening = False
        self.listener = None  # pynput的Listener
        self.hotkeys: Dict[str, any] = {}  # pynput的HotKey
        # 存储坐标采集的临时数据
        self.captured_coords: Dict[str, Optional[Tuple[int, int]]] = {
            'top_left': None,
            'bottom_right': None
        }
        
        # 优先使用keyboard库（更可靠）
        self.use_keyboard = KEYBOARD_AVAILABLE
        self.keyboard_hotkeys = {}  # 存储keyboard库注册的热键ID
        
        # Windows平台尝试使用win32实现（备选）
        self.win32_service = None
        if IS_WINDOWS and not KEYBOARD_AVAILABLE:
            try:
                from backend.services.hotkey_service_win32 import HotkeyServiceWin32
                self.win32_service = HotkeyServiceWin32()
                print("[热键服务] 使用Windows Win32实现")
            except Exception as e:
                print(f"[热键服务] Win32实现不可用: {e}")
                self.win32_service = None

    def _parse_hotkey_keyboard(self, hotkey_str: str) -> str:
        """解析热键字符串为keyboard库格式"""
        # keyboard库使用 '+' 连接，格式如 'ctrl+alt+1'
        # 直接返回，但需要规范化
        parts = [p.strip().lower() for p in hotkey_str.split('+')]
        # 规范化修饰键名称
        normalized = []
        for part in parts:
            if part == 'control' or part == 'ctrl':
                normalized.append('ctrl')
            elif part == 'alt':
                normalized.append('alt')
            elif part == 'shift':
                normalized.append('shift')
            elif part == 'win' or part == 'cmd' or part == 'super':
                normalized.append('win')
            else:
                normalized.append(part)
        return '+'.join(normalized)
    
    def _parse_hotkey_pynput(self, hotkey_str: str) -> list:
        """解析热键字符串为pynput格式的键列表"""
        if keyboard is None:
            return []
        parts = hotkey_str.lower().split('+')
        keys = []
        for part in parts:
            part = part.strip()
            if part == 'ctrl' or part == 'control':
                keys.append(keyboard.Key.ctrl)
            elif part == 'alt':
                keys.append(keyboard.Key.alt)
            elif part == 'shift':
                keys.append(keyboard.Key.shift)
            elif part == 'cmd' or part == 'win' or part == 'super':
                keys.append(keyboard.Key.cmd)
            elif len(part) == 1:
                keys.append(part)
            else:
                if part.isdigit():
                    keys.append(part)
                else:
                    try:
                        key_attr = getattr(keyboard.Key, part, None)
                        if key_attr:
                            keys.append(key_attr)
                        else:
                            keys.append(part)
                    except AttributeError:
                        keys.append(part)
        return keys

    def register_hotkey(self, hotkey_str: str, callback: Callable) -> bool:
        """注册热键"""
        # 优先使用keyboard库
        if self.use_keyboard:
            try:
                hotkey_normalized = self._parse_hotkey_keyboard(hotkey_str)
                print(f"[keyboard] 注册热键: {hotkey_str} -> {hotkey_normalized}")
                kb_lib.add_hotkey(hotkey_normalized, callback)
                self.keyboard_hotkeys[hotkey_str] = hotkey_normalized
                print(f"[keyboard] ✓ 热键注册成功: {hotkey_str}")
                return True
            except Exception as e:
                print(f"[keyboard] ✗ 注册热键失败 {hotkey_str}: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        # Windows平台备选：win32实现
        if self.win32_service:
            return self.win32_service.register_hotkey(hotkey_str, callback)
        
        # 最后使用pynput实现
        if keyboard is None:
            print("[热键服务] ✗ 没有可用的热键库！")
            return False
        
        try:
            keys = self._parse_hotkey_pynput(hotkey_str)
            if not keys:
                print(f"[pynput] 解析热键失败 {hotkey_str}: 无法解析为有效键")
                return False
            
            print(f"[pynput] 解析热键 {hotkey_str} -> {keys}")
            hotkey = keyboard.HotKey(keys, callback)
            self.hotkeys[hotkey_str] = hotkey
            self.hotkey_handlers[hotkey_str] = callback
            print(f"[pynput] 热键注册成功: {hotkey_str}")
            return True
        except Exception as e:
            print(f"[pynput] 注册热键失败 {hotkey_str}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def unregister_hotkey(self, hotkey_str: str) -> bool:
        """注销热键"""
        if self.win32_service:
            return self.win32_service.unregister_hotkey(hotkey_str)
        
        if hotkey_str in self.hotkeys:
            del self.hotkeys[hotkey_str]
        if hotkey_str in self.hotkey_handlers:
            del self.hotkey_handlers[hotkey_str]
        return True

    def _on_press(self, key):
        """按键按下事件"""
        for hotkey in self.hotkeys.values():
            hotkey.press(key)

    def _on_release(self, key):
        """按键释放事件"""
        for hotkey in self.hotkeys.values():
            hotkey.release(key)
        # ESC键停止监听
        if key == keyboard.Key.esc:
            return False

    def start_listening(self):
        """开始监听热键"""
        # keyboard库不需要单独的监听线程，它自动在后台运行
        if self.use_keyboard:
            self.is_listening = True
            print("[keyboard] 热键监听已启动（后台自动运行）")
            return
        
        # win32实现
        if self.win32_service:
            self.win32_service.start_listening()
            self.is_listening = True
            return
        
        # pynput实现
        if keyboard is None:
            print("[热键服务] ✗ 无法启动监听：没有可用的热键库")
            return
        
        if not self.is_listening:
            self.is_listening = True
            self.listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            self.listener.start()
            print("[pynput] 键盘监听器已启动")

    def stop_listening(self):
        """停止监听热键"""
        # keyboard库：清除所有热键
        if self.use_keyboard:
            try:
                kb_lib.unhook_all_hotkeys()
                self.keyboard_hotkeys.clear()
            except:
                pass
            self.is_listening = False
            return
        
        # win32实现
        if self.win32_service:
            self.win32_service.stop_listening()
            self.is_listening = False
            return
        
        # pynput实现
        self.is_listening = False
        if self.listener:
            self.listener.stop()
            self.listener = None

    def clear_captured_coords(self):
        """清除已采集的坐标"""
        if self.win32_service:
            self.win32_service.clear_captured_coords()
        self.captured_coords = {
            'top_left': None,
            'bottom_right': None
        }

    def get_captured_coords(self) -> Dict[str, Optional[Tuple[int, int]]]:
        """获取已采集的坐标"""
        if self.win32_service:
            return self.win32_service.get_captured_coords()
        return self.captured_coords.copy()
    
    def set_captured_coord(self, coord_type: str, x: int, y: int):
        """设置采集的坐标（统一接口）"""
        if self.win32_service:
            self.win32_service.captured_coords[coord_type] = (x, y)
        self.captured_coords[coord_type] = (x, y)

