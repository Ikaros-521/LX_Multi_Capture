import React, { useState, useEffect } from 'react'
import { regionAPI } from '../services/api'

const RegionList = ({ regions, onRefresh, onEdit, onDelete }) => {
  const [previews, setPreviews] = useState({})

  useEffect(() => {
    // 加载所有选区的预览图
    const loadPreviews = async () => {
      const previewMap = {}
      for (const region of regions) {
        try {
          const response = await regionAPI.getPreview(region.id)
          const blob = new Blob([response.data])
          const url = URL.createObjectURL(blob)
          previewMap[region.id] = url
        } catch (error) {
          console.error(`加载预览图失败 ${region.id}:`, error)
        }
      }
      setPreviews(previewMap)
    }
    if (regions.length > 0) {
      loadPreviews()
    }
    return () => {
      // 清理URL对象
      Object.values(previews).forEach(url => URL.revokeObjectURL(url))
    }
  }, [regions])

  if (regions.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        暂无选区，请创建新选区
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {regions.map(region => (
        <div key={region.id} className="border rounded-lg p-4 bg-white shadow-sm">
          <div className="mb-2">
            <h3 className="font-semibold text-lg">{region.name}</h3>
            <p className="text-sm text-gray-600">
              坐标: ({region.x1}, {region.y1}) - ({region.x2}, {region.y2})
            </p>
            <p className="text-xs text-gray-400">
              尺寸: {Math.abs(region.x2 - region.x1)} × {Math.abs(region.y2 - region.y1)}
            </p>
          </div>
          {previews[region.id] && (
            <div className="mb-2">
              <img
                src={previews[region.id]}
                alt={region.name}
                className="w-full h-32 object-contain border rounded"
              />
            </div>
          )}
          <div className="flex gap-2">
            <button
              onClick={() => onEdit(region)}
              className="flex-1 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
            >
              编辑
            </button>
            <button
              onClick={() => onDelete(region.id)}
              className="flex-1 px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
            >
              删除
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

export default RegionList

