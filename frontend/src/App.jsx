import React, { useState, useEffect } from 'react'
import { regionAPI } from './services/api'
import RegionList from './components/RegionList'
import RegionForm from './components/RegionForm'
import ConfigPanel from './components/ConfigPanel'
import ScreenshotControl from './components/ScreenshotControl'
import { useToast } from './contexts/ToastContext'

function App() {
  const [regions, setRegions] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [showConfig, setShowConfig] = useState(false)
  const [editingRegion, setEditingRegion] = useState(null)
  const [loading, setLoading] = useState(false)
  const toast = useToast()

  useEffect(() => {
    loadRegions()
  }, [])

  const loadRegions = async () => {
    setLoading(true)
    try {
      const response = await regionAPI.getAll()
      setRegions(response.data)
    } catch (error) {
      console.error('加载选区失败:', error)
      toast.error('加载选区失败: ' + (error.response?.data?.detail || error.message))
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = () => {
    setEditingRegion(null)
    setShowForm(true)
  }

  const handleEdit = (region) => {
    setEditingRegion(region)
    setShowForm(true)
  }

  const handleSave = async (data) => {
    try {
      if (editingRegion) {
        await regionAPI.update(editingRegion.id, data)
      } else {
        await regionAPI.create(data)
      }
      setShowForm(false)
      setEditingRegion(null)
      toast.success('保存成功')
      loadRegions()
    } catch (error) {
      toast.error('保存失败: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('确定要删除这个选区吗？')) {
      return
    }
    try {
      await regionAPI.delete(id)
      toast.success('删除成功')
      loadRegions()
    } catch (error) {
      toast.error('删除失败: ' + (error.response?.data?.detail || error.message))
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">洛曦 多选区截图器</h1>
            <div className="flex gap-2">
              <button
                onClick={handleCreate}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                创建选区
              </button>
              <button
                onClick={() => setShowConfig(true)}
                className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
              >
                配置
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="mb-6">
          <ScreenshotControl regions={regions} onScreenshot={loadRegions} />
        </div>

        <div className="mb-4">
          <h2 className="text-xl font-semibold mb-4">选区列表</h2>
          {loading ? (
            <div className="text-center py-8">加载中...</div>
          ) : (
            <RegionList
              regions={regions}
              onRefresh={loadRegions}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          )}
        </div>
      </main>

      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="w-full max-w-2xl">
            <RegionForm
              region={editingRegion}
              onSave={handleSave}
              onCancel={() => {
                setShowForm(false)
                setEditingRegion(null)
              }}
            />
          </div>
        </div>
      )}

      {showConfig && (
        <ConfigPanel onClose={() => setShowConfig(false)} />
      )}
    </div>
  )
}

export default App

