# 快速启动指南

## 快速开始（5分钟）

### 1. 安装依赖

**后端：**
```bash
pip install -r requirements.txt
```

**前端：**
```bash
cd frontend
npm install
cd ..
```

### 2. 启动应用

#### 开发模式（推荐）

**Windows:**
- 打开两个命令行窗口
- 窗口1：运行 `start_backend.bat`
- 窗口2：运行 `start_frontend.bat`
- 访问 `http://localhost:5173`

**Linux/Mac:**
- 打开两个终端
- 终端1：运行 `chmod +x start_backend.sh && ./start_backend.sh`
- 终端2：运行 `chmod +x start_frontend.sh && ./start_frontend.sh`
- 访问 `http://localhost:5173`

#### 生产模式

1. 构建前端：
   ```bash
   # Windows
   build_frontend.bat
   
   # Linux/Mac
   chmod +x build_frontend.sh && ./build_frontend.sh
   ```

2. 启动后端：
   ```bash
   # Windows
   start_backend.bat
   
   # Linux/Mac
   chmod +x start_backend.sh && ./start_backend.sh
   ```

3. 访问 `http://localhost:8021`

### 3. 首次使用

1. **创建选区**：
   - 点击"创建选区"
   - 选择"交互式设置（使用热键）"
   - 将鼠标移到目标区域左上角，按 `Ctrl+Alt+1`
   - 将鼠标移到目标区域右下角，按 `Ctrl+Alt+2`
   - 确认预览图，输入名称，保存

2. **截图**：
   - 点击"截取所有选区"按钮
   - 或使用热键 `Ctrl+Alt+S`

3. **配置**：
   - 点击"配置"按钮
   - 设置输出目录和热键

## 常见问题

**Q: 热键不工作？**
A: 确保没有其他程序占用相同热键，Windows上可能需要管理员权限。

**Q: 截图保存到哪里？**
A: 默认保存在 `./screenshots` 目录，可在配置中修改。

**Q: 如何修改热键？**
A: 点击"配置"按钮，修改热键A/B/C的设置。

## 下一步

查看 [README.md](README.md) 获取完整文档。

