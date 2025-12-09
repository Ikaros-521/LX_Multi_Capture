import React, { useState, useEffect } from 'react'
import { regionAPI, mouseAPI, screenshotAPI } from '../services/api'
import { useToast } from '../contexts/ToastContext'

const RegionForm = ({ region, onSave, onCancel, onCapture }) => {
  const toast = useToast()
  const [name, setName] = useState(region?.name || '')
  const [x1, setX1] = useState(region?.x1 || 0)
  const [y1, setY1] = useState(region?.y1 || 0)
  const [x2, setX2] = useState(region?.x2 || 0)
  const [y2, setY2] = useState(region?.y2 || 0)
  const [isCapturing, setIsCapturing] = useState(false)
  const [preview, setPreview] = useState(null)
  const [currentStep, setCurrentStep] = useState('form') // 'form' | 'capturing' | 'preview'

  useEffect(() => {
    if (region) {
      setName(region.name)
      setX1(region.x1)
      setY1(region.y1)
      setX2(region.x2)
      setY2(region.y2)
    }
  }, [region])

  const handleStartCapture = async () => {
    // 清除之前的轮询
    if (window.capturePollInterval) {
      clearInterval(window.capturePollInterval)
      window.capturePollInterval = null
    }
    
    setIsCapturing(true)
    setCurrentStep('capturing')
    try {
      // 清除之前的坐标
      await mouseAPI.clearCoords()
      
      // 开始轮询坐标
      const pollInterval = setInterval(async () => {
        try {
          const response = await mouseAPI.getCapturedCoords()
          const coords = response.data
          
          if (coords.top_left && coords.top_left.length === 2) {
            setX1(coords.top_left[0])
            setY1(coords.top_left[1])
          }
          if (coords.bottom_right && coords.bottom_right.length === 2) {
            setX2(coords.bottom_right[0])
            setY2(coords.bottom_right[1])
          }
          
          // 两个坐标都采集完成，自动进入预览
          if (coords.top_left && coords.bottom_right && 
              coords.top_left.length === 2 && coords.bottom_right.length === 2) {
            clearInterval(pollInterval)
            window.capturePollInterval = null
            setIsCapturing(false)
            setCurrentStep('preview')
          }
        } catch (error) {
          console.error('获取坐标失败:', error)
        }
      }, 300) // 每300ms轮询一次（降低频率）
      
      // 存储interval ID以便清理
      window.capturePollInterval = pollInterval
    } catch (error) {
      console.error('启动坐标采集失败:', error)
      setIsCapturing(false)
      setCurrentStep('form')
    }
  }

  const handleSave = () => {
    if (!name.trim()) {
      toast.warning('请输入选区名称')
      return
    }
    if (x1 === x2 || y1 === y2) {
      toast.warning('选区宽度或高度不能为0')
      return
    }
    onSave({ name, x1, y1, x2, y2 })
  }

  const loadPreview = async () => {
    if (region?.id) {
      // 已有选区，加载其预览
      try {
        const response = await regionAPI.getPreview(region.id)
        const blob = new Blob([response.data])
        const url = URL.createObjectURL(blob)
        setPreview(url)
      } catch (error) {
        console.error('加载预览图失败:', error)
      }
    } else if (x1 && y1 && x2 && y2 && currentStep === 'preview') {
      // 新选区，使用临时预览API
      try {
        const response = await regionAPI.getTempPreview({ name: 'temp', x1, y1, x2, y2 })
        const blob = new Blob([response.data])
        const url = URL.createObjectURL(blob)
        setPreview(url)
      } catch (error) {
        console.error('生成预览图失败:', error)
      }
    }
  }

  useEffect(() => {
    if (currentStep === 'preview') {
      loadPreview()
    }
  }, [region, currentStep, x1, y1, x2, y2])

  // 清理函数
  useEffect(() => {
    return () => {
      // 组件卸载时清理轮询
      if (window.capturePollInterval) {
        clearInterval(window.capturePollInterval)
        window.capturePollInterval = null
      }
      // 清理预览图URL
      if (preview) {
        URL.revokeObjectURL(preview)
      }
    }
  }, [preview])

  if (currentStep === 'capturing') {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-md">
          <h2 className="text-xl font-bold mb-4">坐标采集模式</h2>
          <div className="space-y-2 mb-4">
            <p className="text-sm">
              <strong>步骤1:</strong> 将鼠标移到目标区域左上角，按下 <kbd className="px-2 py-1 bg-gray-200 rounded">Ctrl+Alt+1</kbd>
            </p>
            <p className="text-sm">
              <strong>步骤2:</strong> 将鼠标移到目标区域右下角，按下 <kbd className="px-2 py-1 bg-gray-200 rounded">Ctrl+Alt+2</kbd>
            </p>
          </div>
          <div className="text-sm text-gray-600 mb-4 space-y-1">
            <p className={x1 && y1 ? "text-green-600 font-semibold" : "text-gray-400"}>
              左上角: {x1 && y1 ? `(${x1}, ${y1})` : '未采集'}
            </p>
            <p className={x2 && y2 ? "text-green-600 font-semibold" : "text-gray-400"}>
              右下角: {x2 && y2 ? `(${x2}, ${y2})` : '未采集'}
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={async () => {
                // 停止轮询
                if (window.capturePollInterval) {
                  clearInterval(window.capturePollInterval)
                  window.capturePollInterval = null
                }
                // 清除坐标
                try {
                  await mouseAPI.clearCoords()
                } catch (error) {
                  console.error('清除坐标失败:', error)
                }
                setIsCapturing(false)
                setCurrentStep('form')
              }}
              className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
            >
              取消
            </button>
            <button
              onClick={async () => {
                setIsCapturing(false)
                setCurrentStep('preview')
                if (window.capturePollInterval) {
                  clearInterval(window.capturePollInterval)
                  window.capturePollInterval = null
                }
                // 获取最终坐标
                try {
                  const response = await mouseAPI.getCapturedCoords()
                  const coords = response.data
                  if (coords.top_left) {
                    setX1(coords.top_left[0])
                    setY1(coords.top_left[1])
                  }
                  if (coords.bottom_right) {
                    setX2(coords.bottom_right[0])
                    setY2(coords.bottom_right[1])
                  }
                } catch (error) {
                  console.error('获取坐标失败:', error)
                }
              }}
              className="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              完成采集
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (currentStep === 'preview' && preview) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6 max-w-2xl">
          <h2 className="text-xl font-bold mb-4">预览并确认</h2>
          <div className="mb-4">
            <img src={preview} alt="预览" className="max-w-full max-h-96 border rounded" />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">选区名称</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              placeholder="例如: price, title"
            />
          </div>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium mb-1">左上角 X</label>
              <input
                type="number"
                value={x1}
                onChange={(e) => setX1(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">左上角 Y</label>
              <input
                type="number"
                value={y1}
                onChange={(e) => setY1(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">右下角 X</label>
              <input
                type="number"
                value={x2}
                onChange={(e) => setX2(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">右下角 Y</label>
              <input
                type="number"
                value={y2}
                onChange={(e) => setY2(parseInt(e.target.value) || 0)}
                className="w-full px-3 py-2 border rounded"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => {
                setCurrentStep('form')
                setPreview(null)
                if (preview) URL.revokeObjectURL(preview)
              }}
              className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
            >
              返回
            </button>
            <button
              onClick={handleSave}
              className="flex-1 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            >
              保存
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">
        {region ? '编辑选区' : '创建新选区'}
      </h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">选区名称</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            placeholder="例如: price, title"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">左上角 X</label>
            <input
              type="number"
              value={x1}
              onChange={(e) => setX1(parseInt(e.target.value) || 0)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">左上角 Y</label>
            <input
              type="number"
              value={y1}
              onChange={(e) => setY1(parseInt(e.target.value) || 0)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">右下角 X</label>
            <input
              type="number"
              value={x2}
              onChange={(e) => setX2(parseInt(e.target.value) || 0)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">右下角 Y</label>
            <input
              type="number"
              value={y2}
              onChange={(e) => setY2(parseInt(e.target.value) || 0)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
        </div>
        <div className="flex gap-2">
          {!region && (
            <button
              onClick={handleStartCapture}
              className="flex-1 px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
            >
              交互式设置（使用热键）
            </button>
          )}
          <button
            onClick={handleSave}
            className="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            保存
          </button>
          <button
            onClick={onCancel}
            className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  )
}

export default RegionForm

