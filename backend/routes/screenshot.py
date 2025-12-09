"""
截图路由
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from backend.models import ScreenshotResponse
from backend.services.region_service import RegionService
from backend.services.screenshot_service import ScreenshotService

router = APIRouter(prefix="/api/screenshot", tags=["screenshot"])
region_service = RegionService()
screenshot_service = ScreenshotService()


# 注意：更具体的路由必须在更通用的路由之前
@router.post("/all", response_model=List[ScreenshotResponse])
async def capture_all_regions():
    """截取所有选区"""
    from backend.services.region_service import RegionService
    from backend.services.screenshot_service import ScreenshotService
    
    region_service = RegionService()
    screenshot_service = ScreenshotService()
    
    regions = region_service.get_all_regions()
    if not regions:
        raise HTTPException(status_code=400, detail="没有可用的选区")
    
    results = []
    for region in regions:
        success, message, file_path = screenshot_service.capture_and_save_region(region)
        results.append(ScreenshotResponse(
            success=success,
            message=message,
            file_path=file_path
        ))
    
    return results


@router.post("/{region_id}", response_model=ScreenshotResponse)
async def capture_region(region_id: str):
    """截取指定选区"""
    region = region_service.get_region_by_id(region_id)
    if region is None:
        raise HTTPException(status_code=404, detail="选区不存在")
    
    success, message, file_path = screenshot_service.capture_and_save_region(region)
    if not success:
        raise HTTPException(status_code=500, detail=message)
    
    return ScreenshotResponse(success=True, message=message, file_path=file_path)

