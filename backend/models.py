"""
数据模型定义
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Region(BaseModel):
    """选区模型"""
    id: Optional[str] = None
    name: str
    x1: int
    y1: int
    x2: int
    y2: int
    created_at: Optional[str] = None

    def normalize(self) -> 'Region':
        """规范化坐标，确保 x1<=x2, y1<=y2"""
        x1, x2 = min(self.x1, self.x2), max(self.x1, self.x2)
        y1, y2 = min(self.y1, self.y2), max(self.y1, self.y2)
        return Region(
            id=self.id,
            name=self.name,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            created_at=self.created_at
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "created_at": self.created_at
        }


class RegionCreate(BaseModel):
    """创建选区请求模型"""
    name: str
    x1: int
    y1: int
    x2: int
    y2: int


class RegionUpdate(BaseModel):
    """更新选区请求模型"""
    name: Optional[str] = None
    x1: Optional[int] = None
    y1: Optional[int] = None
    x2: Optional[int] = None
    y2: Optional[int] = None


class HotkeyConfig(BaseModel):
    """热键配置模型"""
    hotkey_a: str = "ctrl+alt+1"  # 记录左上角
    hotkey_b: str = "ctrl+alt+2"  # 记录右下角
    hotkey_c: str = "ctrl+alt+s"  # 手动截图


class AppConfig(BaseModel):
    """应用配置模型"""
    output_dir: str = "./screenshots"
    hotkey_a: str = "ctrl+alt+1"
    hotkey_b: str = "ctrl+alt+2"
    hotkey_c: str = "ctrl+alt+s"
    screenshot_interval: int = 0  # 0表示关闭定时截图


class MousePosition(BaseModel):
    """鼠标位置模型"""
    x: int
    y: int


class ScreenshotResponse(BaseModel):
    """截图响应模型"""
    success: bool
    message: str
    file_path: Optional[str] = None

