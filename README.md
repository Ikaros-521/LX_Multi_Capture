<div align="center">
  <a href="#">
    <img src="https://raw.githubusercontent.com/LuoXi-Project/LX_Project_Template/refs/heads/main/ui/logo.png" width="240" height="240" alt="点我跳转文档">
  </a>
</div>

<div align="center">

# ✨ 洛曦 多选区截图器 ✨

[![][python]][python]
[![][github-release-shield]][github-release-link]
[![][github-stars-shield]][github-stars-link]
[![][github-forks-shield]][github-forks-link]
[![][github-issues-shield]][github-issues-link]  
[![][github-contributors-shield]][github-contributors-link]
[![][github-license-shield]][github-license-link]

</div>

# LX Multi Capture - 多选区截图工具

一个基于 BS 架构（浏览器前端 + Python FastAPI 后端）的多选区截图工具，支持 Windows 和 Linux 系统。

## ✨ 功能特性

1. **选区管理**
   - 创建多个命名矩形选区（如 "price", "title"）
   - 每个选区包含名称、左上角 (x1,y1)、右下角 (x2,y2)
   - 支持增删改查和预览（显示缩略图）

2. **交互式选区设置**
   - 通过自定义热键采集坐标
   - 热键 A（默认 Ctrl+Alt+1）：记录左上角坐标
   - 热键 B（默认 Ctrl+Alt+2）：记录右下角坐标
   - 自动显示实时截图预览和坐标确认

3. **截图执行**
   - 支持手动触发（Web 按钮 + 自定义全局热键 C）
   - 支持定时截图（用户设置间隔，单位秒）
   - 截图保存为 `{name}_{timestamp}.png`

4. **配置管理**
   - 输出目录路径（绝对路径）
   - 热键 A/B/C 自定义
   - 定时截图间隔设置

## 🛠️ 技术栈

- **前端**: React + TailwindCSS + Vite
- **后端**: Python + FastAPI
- **截图**: mss
- **热键监听**: pynput / keyboard (Windows)
- **配置持久化**: JSON 文件

## 📋 环境要求

- Python 3.10+
- Node.js 16+ (用于前端开发)
- Windows 或 Linux 系统

## 🚀 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd LX_Multi_Capture
```

### 2. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 3. 安装前端依赖

```bash
cd frontend
npm install
cd ..
```

## 🎯 运行方式

### 开发模式

#### 方式一：分别启动前后端（推荐开发时使用）

**终端 1 - 启动后端：**
```bash
python -m backend.main
```

**终端 2 - 启动前端开发服务器：**
```bash
cd frontend
npm run dev
```

然后访问 `http://localhost:5173`（前端开发服务器会自动代理 API 请求到后端）

#### 方式二：生产模式（前端构建后）

**1. 构建前端：**
```bash
cd frontend
npm run build
cd ..
```

**2. 启动后端（会自动服务前端静态文件）：**
```bash
python -m backend.main
```

然后访问 `http://localhost:8021`

### 生产模式

```bash
# 构建前端
cd frontend
npm run build
cd ..

# 启动后端
python -m backend.main
```

访问 `http://localhost:8021`

## 📖 使用说明

### 1. 创建选区

#### 方法一：手动输入坐标
1. 点击"创建选区"按钮
2. 输入选区名称和坐标（x1, y1, x2, y2）
3. 点击"保存"

#### 方法二：交互式设置（使用热键）
1. 点击"创建选区" → "交互式设置（使用热键）"
2. 将鼠标移到目标区域左上角，按下 **Ctrl+Alt+1**（或配置的热键A）
3. 将鼠标移到目标区域右下角，按下 **Ctrl+Alt+2**（或配置的热键B）
4. 系统会自动显示预览图和坐标，确认后输入名称并保存

### 2. 截图

#### 手动截图
- 点击"截取所有选区"按钮
- 或使用热键 **Ctrl+Alt+S**（或配置的热键C）

#### 定时截图
1. 点击"配置"按钮
2. 设置"定时截图间隔"（秒），0 表示关闭
3. 保存配置后，系统会自动按间隔截图所有选区

### 3. 配置设置

点击"配置"按钮可以设置：
- **输出目录**：截图保存路径（绝对路径）
- **热键 A**：记录左上角坐标（默认：ctrl+alt+1）
- **热键 B**：记录右下角坐标（默认：ctrl+alt+2）
- **热键 C**：手动截图（默认：ctrl+alt+s）
- **定时截图间隔**：自动截图间隔（秒），0 表示关闭

## 📁 项目结构

```
LX_Multi_Capture/
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI 主应用
│   ├── models.py           # 数据模型
│   ├── routes/             # API 路由
│   │   ├── regions.py      # 选区管理
│   │   ├── config.py       # 配置管理
│   │   ├── screenshot.py   # 截图功能
│   │   └── mouse.py        # 鼠标位置
│   └── services/           # 业务服务
│       ├── region_service.py
│       ├── screenshot_service.py
│       ├── hotkey_service.py
│       └── config_service.py
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── App.jsx         # 主应用组件
│   │   ├── components/     # React 组件
│   │   └── services/       # API 服务
│   ├── package.json
│   └── vite.config.js
├── requirements.txt        # Python 依赖
├── config.json            # 配置文件（自动生成）
├── regions.json           # 选区数据（自动生成）
└── screenshots/           # 截图输出目录（自动创建）
```

## 🔧 API 文档

启动后端后，访问 `http://localhost:8021/docs` 查看完整的 API 文档（FastAPI 自动生成）。

主要 API 端点：
- `GET /api/regions` - 获取所有选区
- `POST /api/regions` - 创建选区
- `PUT /api/regions/{id}` - 更新选区
- `DELETE /api/regions/{id}` - 删除选区
- `GET /api/config` - 获取配置
- `PUT /api/config` - 更新配置
- `POST /api/screenshot/all` - 截取所有选区
- `POST /api/screenshot/{id}` - 截取指定选区

## ⚠️ 注意事项

1. **热键权限**：在某些系统上，全局热键可能需要管理员权限
2. **坐标规范化**：系统会自动处理 x1>x2 或 y1>y2 的情况，确保坐标正确
3. **输出目录**：请确保输出目录有写权限，系统会自动创建不存在的目录
4. **热键冲突**：避免与其他应用程序的热键冲突

## 🐛 故障排除

### 热键不工作
- 检查是否有其他程序占用相同热键
- 在 Windows 上，尝试以管理员权限运行
- 在 Linux 上，确保有必要的权限

### 截图失败
- 检查输出目录是否有写权限
- 确认选区坐标是否在屏幕范围内
- 查看后端控制台的错误信息

### 前端无法连接后端
- 确认后端是否在 `http://localhost:8021` 运行
- 检查 CORS 配置（开发模式下已允许所有来源）

## 📝 许可证

查看 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## ⭐️ Star 经历

[![Star History Chart](https://api.star-history.com/svg?repos=Ikaros-521/LX_Multi_Capture&type=Date)](https://star-history.com/#Ikaros-521/LX_Multi_Capture&Date)

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 许可证

GPL3.0 License

[python]: https://img.shields.io/badge/python-3.10+-blue.svg?labelColor=black
[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-black?style=flat-square
[github-action-release-link]: https://github.com/actions/workflows/Ikaros-521/LX_Multi_Capture/release.yml
[github-action-release-shield]: https://img.shields.io/github/actions/workflow/status/Ikaros-521/LX_Multi_Capture/release.yml?label=release&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-action-test-link]: https://github.com/actions/workflows/Ikaros-521/LX_Multi_Capture/test.yml
[github-action-test-shield]: https://img.shields.io/github/actions/workflow/status/Ikaros-521/LX_Multi_Capture/test.yml?label=test&labelColor=black&logo=githubactions&logoColor=white&style=flat-square
[github-codespace-link]: https://codespaces.new/Ikaros-521/LX_Multi_Capture
[github-codespace-shield]: https://github.com/codespaces/badge.svg
[github-contributors-link]: https://github.com/Ikaros-521/LX_Multi_Capture/graphs/contributors
[github-contributors-shield]: https://img.shields.io/github/contributors/Ikaros-521/LX_Multi_Capture?color=c4f042&labelColor=black&style=flat-square
[github-forks-link]: https://github.com/Ikaros-521/LX_Multi_Capture/network/members
[github-forks-shield]: https://img.shields.io/github/forks/Ikaros-521/LX_Multi_Capture?color=8ae8ff&labelColor=black&style=flat-square
[github-issues-link]: https://github.com/Ikaros-521/LX_Multi_Capture/issues
[github-issues-shield]: https://img.shields.io/github/issues/Ikaros-521/LX_Multi_Capture?color=ff80eb&labelColor=black&style=flat-square
[github-license-link]: https://github.com/Ikaros-521/LX_Multi_Capture/blob/main/LICENSE
[github-license-shield]: https://img.shields.io/github/license/Ikaros-521/LX_Multi_Capture?color=white&labelColor=black&style=flat-square
[github-release-link]: https://github.com/Ikaros-521/LX_Multi_Capture/releases
[github-release-shield]: https://img.shields.io/github/v/release/Ikaros-521/LX_Multi_Capture?color=369eff&labelColor=black&logo=github&style=flat-square
[github-releasedate-link]: https://github.com/Ikaros-521/LX_Multi_Capture/releases
[github-releasedate-shield]: https://img.shields.io/github/release-date/Ikaros-521/LX_Multi_Capture?labelColor=black&style=flat-square
[github-stars-link]: https://github.com/Ikaros-521/LX_Multi_Capture/network/stargazers
[github-stars-shield]: https://img.shields.io/github/stars/Ikaros-521/LX_Multi_Capture?color=ffcb47&labelColor=black&style=flat-square
[pr-welcome-link]: https://github.com/Ikaros-521/LX_Multi_Capture/pulls
[pr-welcome-shield]: https://img.shields.io/badge/%F0%9F%A4%AF%20PR%20WELCOME-%E2%86%92-ffcb47?labelColor=black&style=for-the-badge
[profile-link]: https://github.com/LuoXi-Project
