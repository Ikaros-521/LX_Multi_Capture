"""
配置服务：负责配置的加载、保存和管理
"""
import json
import os
from pathlib import Path
from typing import Optional
from backend.models import AppConfig

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "output_dir": "./screenshots",
    "hotkey_a": "ctrl+alt+1",
    "hotkey_b": "ctrl+alt+2",
    "hotkey_c": "ctrl+alt+s",
    "screenshot_interval": 0
}


class ConfigService:
    """配置服务单例"""
    _instance = None
    _config: Optional[AppConfig] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self.load_config()

    def load_config(self) -> AppConfig:
        """加载配置文件"""
        config_path = Path(CONFIG_FILE)
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._config = AppConfig(**data)
            except Exception as e:
                print(f"加载配置失败，使用默认配置: {e}")
                self._config = AppConfig(**DEFAULT_CONFIG)
        else:
            self._config = AppConfig(**DEFAULT_CONFIG)
            self.save_config()
        return self._config

    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                # 兼容Pydantic v1和v2
                config_dict = self._config.dict() if hasattr(self._config, 'dict') else self._config.model_dump()
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def get_config(self) -> AppConfig:
        """获取当前配置"""
        return self._config

    def update_config(self, **kwargs) -> AppConfig:
        """更新配置"""
        # 兼容Pydantic v1和v2
        config_dict = self._config.dict() if hasattr(self._config, 'dict') else self._config.model_dump()
        config_dict.update({k: v for k, v in kwargs.items() if v is not None})
        self._config = AppConfig(**config_dict)
        self.save_config()
        return self._config

    def validate_output_dir(self, path: str) -> tuple[bool, str]:
        """验证输出目录是否可写"""
        try:
            path_obj = Path(path)
            # 如果目录不存在，尝试创建
            if not path_obj.exists():
                path_obj.mkdir(parents=True, exist_ok=True)
            # 检查是否可写
            test_file = path_obj / ".write_test"
            try:
                test_file.write_text("test")
                test_file.unlink()
                return True, "目录验证成功"
            except Exception as e:
                return False, f"目录不可写: {e}"
        except Exception as e:
            return False, f"目录路径无效: {e}"

