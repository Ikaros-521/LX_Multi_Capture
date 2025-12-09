"""
选区服务：负责选区的CRUD操作
"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from backend.models import Region, RegionCreate, RegionUpdate

REGIONS_FILE = "regions.json"


class RegionService:
    """选区服务"""
    
    def __init__(self):
        self.regions: List[Region] = []
        self.load_regions()

    def load_regions(self):
        """从文件加载选区"""
        regions_path = Path(REGIONS_FILE)
        if regions_path.exists():
            try:
                with open(regions_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.regions = [Region(**item) for item in data]
            except Exception as e:
                print(f"加载选区失败: {e}")
                self.regions = []
        else:
            self.regions = []

    def save_regions(self) -> bool:
        """保存选区到文件"""
        try:
            with open(REGIONS_FILE, 'w', encoding='utf-8') as f:
                data = [region.to_dict() for region in self.regions]
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存选区失败: {e}")
            return False

    def get_all_regions(self) -> List[Region]:
        """获取所有选区"""
        return self.regions

    def get_region_by_id(self, region_id: str) -> Optional[Region]:
        """根据ID获取选区"""
        for region in self.regions:
            if region.id == region_id:
                return region
        return None

    def create_region(self, region_data: RegionCreate) -> Region:
        """创建选区"""
        region = Region(
            id=str(uuid.uuid4()),
            name=region_data.name,
            x1=region_data.x1,
            y1=region_data.y1,
            x2=region_data.x2,
            y2=region_data.y2,
            created_at=datetime.now().isoformat()
        )
        # 规范化坐标
        region = region.normalize()
        self.regions.append(region)
        self.save_regions()
        return region

    def update_region(self, region_id: str, region_data: RegionUpdate) -> Optional[Region]:
        """更新选区"""
        region = self.get_region_by_id(region_id)
        if region is None:
            return None
        
        # 更新字段
        if region_data.name is not None:
            region.name = region_data.name
        if region_data.x1 is not None:
            region.x1 = region_data.x1
        if region_data.y1 is not None:
            region.y1 = region_data.y1
        if region_data.x2 is not None:
            region.x2 = region_data.x2
        if region_data.y2 is not None:
            region.y2 = region_data.y2
        
        # 规范化坐标
        region = region.normalize()
        self.save_regions()
        return region

    def delete_region(self, region_id: str) -> bool:
        """删除选区"""
        region = self.get_region_by_id(region_id)
        if region is None:
            return False
        
        self.regions.remove(region)
        self.save_regions()
        return True

