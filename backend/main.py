"""
FastAPI主应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import threading
import time

from backend.routes import regions, config, screenshot, mouse
from backend.services.hotkey_service import HotkeyService
from backend.services.config_service import ConfigService
from backend.services.region_service import RegionService
from backend.services.screenshot_service import ScreenshotService

# 全局服务实例
hotkey_service = HotkeyService()
config_service = ConfigService()
region_service = RegionService()
screenshot_service = ScreenshotService()

app = FastAPI(
    title="LX Multi Capture API",
    description="多选区截图工具API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由（必须在静态文件之前，确保API路由优先）
app.include_router(regions.router)
app.include_router(config.router)
app.include_router(screenshot.router)
app.include_router(mouse.router)

# 静态文件服务（前端构建后的文件）- 必须在API路由之后挂载
frontend_path = Path("frontend/dist")
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")

# 定时截图相关
screenshot_timer_running = False
screenshot_timer_thread = None


def screenshot_timer_worker():
    """定时截图工作线程"""
    global screenshot_timer_running
    while screenshot_timer_running:
        config = config_service.get_config()
        if config.screenshot_interval > 0:
            # 每次循环重新加载最新的选区配置，避免使用旧数据
            try:
                region_service.load_regions()
            except Exception as e:
                print(f"[定时截图] 重新加载选区失败: {e}")
            regions = region_service.get_all_regions()
            for region in regions:
                screenshot_service.capture_and_save_region(region)
            time.sleep(config.screenshot_interval)
        else:
            time.sleep(1)


def start_screenshot_timer():
    """启动定时截图"""
    global screenshot_timer_running, screenshot_timer_thread
    if not screenshot_timer_running:
        screenshot_timer_running = True
        screenshot_timer_thread = threading.Thread(target=screenshot_timer_worker, daemon=True)
        screenshot_timer_thread.start()


def stop_screenshot_timer():
    """停止定时截图"""
    global screenshot_timer_running
    screenshot_timer_running = False


# 热键回调函数
def on_hotkey_a():
    """热键A：记录左上角坐标"""
    print("\n" + "=" * 60)
    print("[热键A] ========== 触发！==========")
    try:
        from backend.utils.platform_utils import get_mouse_position
        print("[热键A] 正在获取鼠标位置...")
        pos = get_mouse_position()
        print(f"[热键A] 获取到坐标: {pos}")
        
        hotkey_service.set_captured_coord('top_left', pos[0], pos[1])
        current_coords = hotkey_service.get_captured_coords()
        print(f"[热键A] 已保存坐标: {current_coords}")
        print(f"[热键A] ========== 完成 ==========")
    except Exception as e:
        print(f"[热键A] ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    print("=" * 60 + "\n")


def on_hotkey_b():
    """热键B：记录右下角坐标"""
    print("\n" + "=" * 60)
    print("[热键B] ========== 触发！==========")
    try:
        from backend.utils.platform_utils import get_mouse_position
        print("[热键B] 正在获取鼠标位置...")
        pos = get_mouse_position()
        print(f"[热键B] 获取到坐标: {pos}")
        
        hotkey_service.set_captured_coord('bottom_right', pos[0], pos[1])
        current_coords = hotkey_service.get_captured_coords()
        print(f"[热键B] 已保存坐标: {current_coords}")
        print(f"[热键B] ========== 完成 ==========")
    except Exception as e:
        print(f"[热键B] ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    print("=" * 60 + "\n")


def on_hotkey_c():
    """热键C：手动截图"""
    print("\n" + "=" * 60)
    print("[热键C] ========== 触发！执行截图 ==========")
    try:
        regions = region_service.get_all_regions()
        if not regions:
            print("[热键C] ⚠ 警告: 没有可用的选区")
            return
        
        print(f"[热键C] 找到 {len(regions)} 个选区，开始截图...")
        success_count = 0
        for region in regions:
            try:
                success, message, file_path = screenshot_service.capture_and_save_region(region)
                if success:
                    success_count += 1
                    print(f"[热键C] ✓ {region.name}: {file_path}")
                else:
                    print(f"[热键C] ✗ {region.name}: {message}")
            except Exception as e:
                print(f"[热键C] ✗ {region.name}: 错误 - {e}")
        
        print(f"[热键C] 完成！成功: {success_count}/{len(regions)}")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"[热键C] ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60 + "\n")


def setup_hotkeys():
    """设置热键"""
    try:
        config = config_service.get_config()
        # 先清除旧热键
        hotkey_service.unregister_hotkey(config.hotkey_a)
        hotkey_service.unregister_hotkey(config.hotkey_b)
        hotkey_service.unregister_hotkey(config.hotkey_c)
        
        # 注册新热键
        success_a = hotkey_service.register_hotkey(config.hotkey_a, on_hotkey_a)
        success_b = hotkey_service.register_hotkey(config.hotkey_b, on_hotkey_b)
        success_c = hotkey_service.register_hotkey(config.hotkey_c, on_hotkey_c)
        
        print(f"热键注册结果: A={success_a}, B={success_b}, C={success_c}")
        print(f"热键配置: A={config.hotkey_a}, B={config.hotkey_b}, C={config.hotkey_c}")
        
        # 启动监听
        hotkey_service.start_listening()
        print("热键监听已启动")
    except Exception as e:
        print(f"设置热键失败: {e}")
        import traceback
        traceback.print_exc()


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("应用启动中...")
    # 启动定时截图
    start_screenshot_timer()
    # 设置热键（注意：在某些系统上可能需要管理员权限）
    try:
        setup_hotkeys()
        print("热键注册成功")
    except Exception as e:
        print(f"热键注册失败: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("应用关闭中...")
    stop_screenshot_timer()
    hotkey_service.stop_listening()


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8021,
        reload=False
    )

