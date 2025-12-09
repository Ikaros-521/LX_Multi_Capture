"""
选区管理路由
"""
from fastapi import APIRouter, HTTPException
from typing import List
from backend.models import Region, RegionCreate, RegionUpdate
from backend.services.region_service import RegionService
from backend.services.screenshot_service import ScreenshotService

router = APIRouter(prefix="/api/regions", tags=["regions"])

# 延迟创建服务实例
def get_services():
    """获取服务实例"""
    return RegionService(), ScreenshotService()


@router.get("", response_model=List[Region])
async def get_all_regions():
    """获取所有选区"""
    region_service, _ = get_services()
    return region_service.get_all_regions()


@router.get("/{region_id}", response_model=Region)
async def get_region(region_id: str):
    """根据ID获取选区"""
    region_service, _ = get_services()
    region = region_service.get_region_by_id(region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="选区不存在")
    return region


@router.post("", response_model=Region, status_code=201)
async def create_region(region_data: RegionCreate):
    """创建选区"""
    region_service, _ = get_services()
    # 验证坐标
    if region_data.x1 == region_data.x2 or region_data.y1 == region_data.y2:
        raise HTTPException(status_code=400, detail="选区宽度或高度不能为0")
    
    return region_service.create_region(region_data)


@router.put("/{region_id}", response_model=Region)
async def update_region(region_id: str, region_data: RegionUpdate):
    """更新选区"""
    region_service, _ = get_services()
    region = region_service.update_region(region_id, region_data)
    if region is None:
        raise HTTPException(status_code=404, detail="选区不存在")
    return region


@router.delete("/{region_id}", status_code=204)
async def delete_region(region_id: str):
    """删除选区"""
    region_service, _ = get_services()
    success = region_service.delete_region(region_id)
    if not success:
        raise HTTPException(status_code=404, detail="选区不存在")


@router.get("/{region_id}/preview")
async def get_region_preview(region_id: str):
    """获取选区预览图"""
    region_service, screenshot_service = get_services()
    region = region_service.get_region_by_id(region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="选区不存在")
    
    preview_data = screenshot_service.get_region_preview(region)
    if preview_data is None:
        raise HTTPException(status_code=500, detail="生成预览图失败")
    
    from fastapi.responses import Response
    return Response(content=preview_data, media_type="image/png")


@router.post("/preview-temp")
async def get_temp_preview(region_data: RegionCreate):
    """获取临时选区预览图（用于交互式设置）"""
    from backend.models import Region
    _, screenshot_service = get_services()
    
    # 创建临时选区对象
    temp_region = Region(
        name="temp",
        x1=region_data.x1,
        y1=region_data.y1,
        x2=region_data.x2,
        y2=region_data.y2
    )
    
    preview_data = screenshot_service.get_region_preview(temp_region)
    if preview_data is None:
        raise HTTPException(status_code=500, detail="生成预览图失败")
    
    from fastapi.responses import Response
    return Response(content=preview_data, media_type="image/png")

