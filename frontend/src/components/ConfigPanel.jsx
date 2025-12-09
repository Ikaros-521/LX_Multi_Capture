import React, { useState, useEffect } from 'react'
import { configAPI } from '../services/api'
import { useToast } from '../contexts/ToastContext'

const ConfigPanel = ({ onClose }) => {
  const toast = useToast()
  const [config, setConfig] = useState({
    output_dir: './screenshots',
    hotkey_a: 'ctrl+alt+1',
    hotkey_b: 'ctrl+alt+2',
    hotkey_c: 'ctrl+alt+s',
    screenshot_interval: 0
  })
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadConfig()
  }, [])

  const loadConfig = async () => {
    try {
      const response = await configAPI.get()
      setConfig(response.data)
    } catch (error) {
      console.error('加载配置失败:', error)
    }
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      // 验证输出目录
      const validateResponse = await configAPI.validateOutputDir(config.output_dir)
      if (!validateResponse.data.valid) {
        toast.error(`目录验证失败: ${validateResponse.data.message}`)
        setLoading(false)
        return
      }

      await configAPI.update(config)
      toast.success('配置保存成功！')
      setTimeout(() => {
        onClose()
      }, 500)
    } catch (error) {
      toast.error(`保存失败: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">配置设置</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">输出目录（绝对路径）</label>
            <input
              type="text"
              value={config.output_dir}
              onChange={(e) => setConfig({ ...config, output_dir: e.target.value })}
              className="w-full px-3 py-2 border rounded"
              placeholder="例如: D:\screenshots 或 /home/user/screenshots"
            />
            <p className="text-xs text-gray-500 mt-1">截图文件将保存到此目录</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">热键 A - 记录左上角坐标</label>
            <input
              type="text"
              value={config.hotkey_a}
              onChange={(e) => setConfig({ ...config, hotkey_a: e.target.value })}
              className="w-full px-3 py-2 border rounded"
              placeholder="例如: ctrl+alt+1"
            />
            <p className="text-xs text-gray-500 mt-1">格式: ctrl+alt+1, shift+ctrl+a 等</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">热键 B - 记录右下角坐标</label>
            <input
              type="text"
              value={config.hotkey_b}
              onChange={(e) => setConfig({ ...config, hotkey_b: e.target.value })}
              className="w-full px-3 py-2 border rounded"
              placeholder="例如: ctrl+alt+2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">热键 C - 手动截图</label>
            <input
              type="text"
              value={config.hotkey_c}
              onChange={(e) => setConfig({ ...config, hotkey_c: e.target.value })}
              className="w-full px-3 py-2 border rounded"
              placeholder="例如: ctrl+alt+s"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">定时截图间隔（秒）</label>
            <input
              type="number"
              value={config.screenshot_interval}
              onChange={(e) => setConfig({ ...config, screenshot_interval: parseInt(e.target.value) || 0 })}
              className="w-full px-3 py-2 border rounded"
              min="0"
            />
            <p className="text-xs text-gray-500 mt-1">0 表示关闭定时截图</p>
          </div>
        </div>

        <div className="flex gap-2 mt-6">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            取消
          </button>
          <button
            onClick={handleSave}
            disabled={loading}
            className="flex-1 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {loading ? '保存中...' : '保存'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ConfigPanel

