import React from 'react'
import { screenshotAPI } from '../services/api'
import { useToast } from '../contexts/ToastContext'

const ScreenshotControl = ({ regions, onScreenshot }) => {
  const toast = useToast()
  const handleCaptureAll = async () => {
    try {
      const response = await screenshotAPI.captureAll()
      const results = response.data
      const successCount = results.filter(r => r.success).length
      if (successCount === results.length) {
        toast.success(`截图完成！成功: ${successCount}/${results.length}`)
      } else {
        toast.warning(`截图完成！成功: ${successCount}/${results.length}`)
      }
      if (onScreenshot) {
        onScreenshot()
      }
    } catch (error) {
      toast.error(`截图失败: ${error.response?.data?.detail || error.message}`)
    }
  }

  const handleCaptureOne = async (regionId) => {
    try {
      const response = await screenshotAPI.capture(regionId)
      toast.success(`截图成功！文件: ${response.data.file_path}`)
      if (onScreenshot) {
        onScreenshot()
      }
    } catch (error) {
      toast.error(`截图失败: ${error.response?.data?.detail || error.message}`)
    }
  }

  if (regions.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-4 text-center text-gray-500">
        请先创建选区
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="font-semibold mb-3">截图控制</h3>
      <div className="space-y-2">
        <button
          onClick={handleCaptureAll}
          className="w-full px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          截取所有选区
        </button>
        <div className="text-sm text-gray-600 mt-2">
          <p>或使用热键 <kbd className="px-2 py-1 bg-gray-200 rounded">Ctrl+Alt+S</kbd> 手动截图</p>
        </div>
      </div>
    </div>
  )
}

export default ScreenshotControl

