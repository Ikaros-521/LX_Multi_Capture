"""
配置管理路由
"""
from fastapi import APIRouter, HTTPException
from backend.models import AppConfig
from backend.services.config_service import ConfigService

router = APIRouter(prefix="/api/config", tags=["config"])

def get_config_service():
    """获取配置服务实例"""
    return ConfigService()


@router.get("", response_model=AppConfig)
async def get_config():
    """获取当前配置"""
    config_service = get_config_service()
    return config_service.get_config()


@router.put("", response_model=AppConfig)
async def update_config(config: AppConfig):
    """更新配置"""
    config_service = get_config_service()
    # 验证输出目录
    if config.output_dir:
        is_valid, message = config_service.validate_output_dir(config.output_dir)
        if not is_valid:
            raise HTTPException(status_code=400, detail=message)
    
    # 兼容Pydantic v1和v2
    config_dict = config.dict() if hasattr(config, 'dict') else config.model_dump()
    updated_config = config_service.update_config(**config_dict)
    return updated_config


@router.post("/validate-output-dir")
async def validate_output_dir(path: str):
    """验证输出目录"""
    config_service = get_config_service()
    is_valid, message = config_service.validate_output_dir(path)
    return {"valid": is_valid, "message": message}

