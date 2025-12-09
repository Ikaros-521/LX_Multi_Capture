"""
截图服务：负责屏幕截图功能
"""
import mss
from PIL import Image
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
from backend.models import Region
from backend.services.config_service import ConfigService


class ScreenshotService:
    """截图服务"""
    
    def __init__(self):
        self.config_service = ConfigService()
        # mss实例不能跨线程使用，每次使用时创建新实例
        self._mss_instance = None
    
    def _get_mss_instance(self):
        """获取mss实例（线程安全）"""
        # 每个线程使用独立的mss实例
        import threading
        if not hasattr(threading.current_thread(), '_mss_instance'):
            threading.current_thread()._mss_instance = mss.mss()
        return threading.current_thread()._mss_instance

    def capture_region(self, region: Region) -> Optional[Image.Image]:
        """截取指定区域"""
        try:
            # 规范化坐标
            normalized = region.normalize()
            # mss使用(left, top, width, height)
            left = normalized.x1
            top = normalized.y1
            width = normalized.x2 - normalized.x1
            height = normalized.y2 - normalized.y1
            
            if width <= 0 or height <= 0:
                return None
            
            monitor = {
                "left": left,
                "top": top,
                "width": width,
                "height": height
            }
            
            # 使用线程安全的mss实例
            mss_instance = self._get_mss_instance()
            screenshot = mss_instance.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            return img
        except Exception as e:
            print(f"截图失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def capture_full_screen(self) -> Optional[Image.Image]:
        """截取全屏"""
        try:
            # 使用线程安全的mss实例
            mss_instance = self._get_mss_instance()
            monitor = mss_instance.monitors[1]  # 主显示器
            screenshot = mss_instance.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            return img
        except Exception as e:
            print(f"全屏截图失败: {e}")
            import traceback
            traceback.print_exc()
            return None

    def save_screenshot(self, img: Image.Image, region_name: str) -> Optional[str]:
        """保存截图到文件"""
        try:
            config = self.config_service.get_config()
            output_dir = Path(config.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"{region_name}_{timestamp}.png"
            file_path = output_dir / filename
            
            img.save(file_path, "PNG")
            return str(file_path)
        except Exception as e:
            print(f"保存截图失败: {e}")
            return None

    def capture_and_save_region(self, region: Region) -> Tuple[bool, str, Optional[str]]:
        """截取并保存区域"""
        try:
            img = self.capture_region(region)
            if img is None:
                print(f"[截图服务] ✗ 截图失败: {region.name}")
                return False, "截图失败", None
            
            file_path = self.save_screenshot(img, region.name)
            if file_path is None:
                print(f"[截图服务] ✗ 保存失败: {region.name}")
                return False, "保存失败", None
            
            print(f"[截图服务] ✓ 成功: {region.name} -> {file_path}")
            return True, "截图成功", file_path
        except Exception as e:
            print(f"[截图服务] ✗ 异常: {region.name} - {e}")
            import traceback
            traceback.print_exc()
            return False, f"异常: {str(e)}", None

    def get_region_preview(self, region: Region, max_size: Tuple[int, int] = (200, 200)) -> Optional[bytes]:
        """获取选区预览图（缩略图）"""
        img = self.capture_region(region)
        if img is None:
            return None
        
        # 生成缩略图
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 转换为bytes
        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

