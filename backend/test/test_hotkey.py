#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试热键功能
"""
import sys
import time
import platform

print("=" * 60)
print("热键功能测试")
print("=" * 60)
print(f"平台: {platform.system()}")
print(f"Python版本: {sys.version}")
print()

# 存储坐标
captured_coords = {
    'top_left': None,
    'bottom_right': None
}

def on_hotkey_a():
    """热键A回调"""
    print("\n" + "=" * 60)
    print("[热键A] 触发！")
    try:
        sys.path.insert(0, '.')
        from backend.utils.platform_utils import get_mouse_position
        pos = get_mouse_position()
        captured_coords['top_left'] = pos
        print(f"[热键A] 记录左上角坐标: {pos}")
        print(f"[热键A] 当前状态: {captured_coords}")
    except Exception as e:
        print(f"[热键A] 错误: {e}")
        import traceback
        traceback.print_exc()
    print("=" * 60)

def on_hotkey_b():
    """热键B回调"""
    print("\n" + "=" * 60)
    print("[热键B] 触发！")
    try:
        sys.path.insert(0, '.')
        from backend.utils.platform_utils import get_mouse_position
        pos = get_mouse_position()
        captured_coords['bottom_right'] = pos
        print(f"[热键B] 记录右下角坐标: {pos}")
        print(f"[热键B] 当前状态: {captured_coords}")
    except Exception as e:
        print(f"[热键B] 错误: {e}")
        import traceback
        traceback.print_exc()
    print("=" * 60)

# 测试热键服务
print("[步骤1] 初始化热键服务...")
try:
    sys.path.insert(0, '.')
    from backend.services.hotkey_service import HotkeyService
    
    hotkey_service = HotkeyService()
    print(f"✓ 热键服务初始化成功")
    
    # 检查实现类型
    if hasattr(hotkey_service, 'use_keyboard') and hotkey_service.use_keyboard:
        print(f"✓ 使用 keyboard 库实现（推荐）")
    elif hasattr(hotkey_service, 'win32_service') and hotkey_service.win32_service:
        print(f"✓ 使用 Win32 实现")
    else:
        print(f"✓ 使用 pynput 实现")
    
    # 注册热键
    print("\n[步骤2] 注册热键...")
    print("  热键A (Ctrl+Alt+1): 记录左上角")
    print("  热键B (Ctrl+Alt+2): 记录右下角")
    
    success_a = hotkey_service.register_hotkey("ctrl+alt+1", on_hotkey_a)
    success_b = hotkey_service.register_hotkey("ctrl+alt+2", on_hotkey_b)
    
    print(f"  热键A注册: {'✓ 成功' if success_a else '✗ 失败'}")
    print(f"  热键B注册: {'✓ 成功' if success_b else '✗ 失败'}")
    
    if not success_a or not success_b:
        print("\n⚠ 警告: 部分热键注册失败，请检查:")
        print("  1. 是否有其他程序占用相同热键")
        print("  2. Windows上是否需要管理员权限")
        print("  3. 查看上面的错误信息")
    
    # 启动监听
    print("\n[步骤3] 启动热键监听...")
    hotkey_service.start_listening()
    print(f"✓ 热键监听已启动")
    print(f"  监听状态: {hotkey_service.is_listening}")
    
    print("\n" + "=" * 60)
    print("热键测试运行中...")
    print("=" * 60)
    print("请按以下热键测试:")
    print("  - Ctrl+Alt+1: 记录左上角坐标")
    print("  - Ctrl+Alt+2: 记录右下角坐标")
    print("  - Ctrl+C: 退出测试")
    print("=" * 60)
    print()
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
            # 显示当前状态
            if captured_coords['top_left'] or captured_coords['bottom_right']:
                print(f"\r当前坐标状态: {captured_coords}", end='', flush=True)
    except KeyboardInterrupt:
        print("\n\n[退出] 停止热键监听...")
        hotkey_service.stop_listening()
        print("✓ 测试结束")
        print(f"\n最终坐标状态: {captured_coords}")
    
except Exception as e:
    print(f"\n✗ 错误: {e}")
    import traceback
    traceback.print_exc()
    print("\n请检查:")
    print("  1. 是否安装了所有依赖: pip install -r requirements.txt")
    print("  2. 是否安装了keyboard库: pip install keyboard")
    print("  3. Windows上是否安装了: pip install pyautogui pywin32")
    print("  4. 查看上面的错误信息")

