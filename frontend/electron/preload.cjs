const { contextBridge } = require('electron')

// 暴露空白api占位，后续可扩展
contextBridge.exposeInMainWorld('api', {})

