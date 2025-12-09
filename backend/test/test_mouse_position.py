#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试鼠标位置获取功能
"""
import sys
import time

print("=" * 60)
print("鼠标位置获取测试")
print("=" * 60)

# 测试1: pyautogui
print("\n[测试1] 使用 pyautogui")
try:
    import pyautogui
    print(f"✓ pyautogui 可用")
    for i in range(3):
        pos = pyautogui.position()
        print(f"  第{i+1}次: ({pos.x}, {pos.y})")
        time.sleep(0.5)
except ImportError:
    print("✗ pyautogui 不可用，请安装: pip install pyautogui")
except Exception as e:
    print(f"✗ pyautogui 错误: {e}")
    import traceback
    traceback.print_exc()

# 测试2: win32api (仅Windows)
if sys.platform == 'win32':
    print("\n[测试2] 使用 win32api (Windows)")
    try:
        import win32api
        print(f"✓ win32api 可用")
        for i in range(3):
            pos = win32api.GetCursorPos()
            print(f"  第{i+1}次: ({pos[0]}, {pos[1]})")
            time.sleep(0.5)
    except ImportError:
        print("✗ win32api 不可用，请安装: pip install pywin32")
    except Exception as e:
        print(f"✗ win32api 错误: {e}")
        import traceback
        traceback.print_exc()

# 测试3: pynput
print("\n[测试3] 使用 pynput")
try:
    from pynput.mouse import Controller
    mouse_controller = Controller()
    print(f"✓ pynput 可用")
    for i in range(3):
        pos = mouse_controller.position
        print(f"  第{i+1}次: ({pos[0]}, {pos[1]})")
        time.sleep(0.5)
except ImportError:
    print("✗ pynput 不可用，请安装: pip install pynput")
except Exception as e:
    print(f"✗ pynput 错误: {e}")
    import traceback
    traceback.print_exc()

# 测试4: 使用平台工具
print("\n[测试4] 使用平台工具 (backend.utils.platform_utils)")
try:
    sys.path.insert(0, '.')
    from backend.utils.platform_utils import get_mouse_position, get_platform_info
    
    platform_info = get_platform_info()
    print(f"平台信息: {platform_info}")
    
    for i in range(3):
        pos = get_mouse_position()
        print(f"  第{i+1}次: {pos}")
        time.sleep(0.5)
except Exception as e:
    print(f"✗ 平台工具错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成！请移动鼠标观察坐标变化")
print("=" * 60)

