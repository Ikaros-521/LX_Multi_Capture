import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 选区API
export const regionAPI = {
  getAll: () => api.get('/regions'),
  getById: (id) => api.get(`/regions/${id}`),
  create: (data) => api.post('/regions', data),
  update: (id, data) => api.put(`/regions/${id}`, data),
  delete: (id) => api.delete(`/regions/${id}`),
  getPreview: (id) => api.get(`/regions/${id}/preview`, { responseType: 'blob' }),
  getTempPreview: (data) => api.post('/regions/preview-temp', data, { responseType: 'blob' })
}

// 配置API
export const configAPI = {
  get: () => api.get('/config'),
  update: (data) => api.put('/config', data),
  validateOutputDir: (path) => api.post('/config/validate-output-dir', null, { params: { path } })
}

// 截图API
export const screenshotAPI = {
  capture: (regionId) => api.post(`/screenshot/${regionId}`),
  captureAll: () => api.post('/screenshot/all')
}

// 鼠标API
export const mouseAPI = {
  getPosition: () => api.get('/mouse/position'),
  getCapturedCoords: () => api.get('/mouse/captured-coords'),
  clearCoords: () => api.post('/mouse/clear-coords')
}

export default api

