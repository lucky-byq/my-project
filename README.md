# 🌿 中药识别 AI 全栈应用

这是我的第一个 Git 项目，一个基于深度学习的中药图像识别全栈应用，采用 **React 前端 + Flask 后端 + TensorFlow 模型** 开发。

---

## ✨ 项目功能
- 提供中药图像智能识别服务，上传图片即可快速预测药材种类
- 前后端分离架构，RESTful API 服务部署，支持跨平台调用
- 基于 TensorFlow 训练的深度学习模型，实现高精度识别

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React |
| 后端 | Flask (Python) |
| 模型 | TensorFlow |

---

## 📂 项目结构
 
'''
my-project/
├── backend/              # Flask 后端模块
│   ├── app.py            # 后端入口文件，提供 API 接口
│   ├── predict_service.py # 模型预测逻辑
│   └── requirements.txt  # Python 依赖清单
├── src/                  # React 前端核心代码
│   ├── App.js            # 主组件，实现图片上传与结果展示
│   ├── App.css           # 主组件样式
│   ├── index.js          # 项目入口文件
│   └── index.css         # 全局样式文件
├── image/                # 示例图片资源文件夹
├── public/               # 前端静态资源文件夹
├── package.json          # 前端依赖配置
└── README.md             # 项目说明文档
'''
---

## 🚀 快速启动

### 后端启动
```bash
# 进入后端目录
cd backend
# 安装依赖
pip install -r requirements.txt
# 启动 Flask 服务（默认端口 5000）
python app.py
 
前端启动
# 进入项目根目录
cd my-project
# 安装依赖
npm install
# 启动 React 项目（默认端口 3000）
npm start
 

☁️ 完整部署说明
 
一、本地部署流程
 
1. 确保本地已安装 Python、Node.js、Git 环境
2. 克隆项目到本地： git clone https://github.com/lucky-byq/my-project.git 
3. 后端：安装 Python 依赖并启动服务（默认端口 5000）
4. 前端：安装 Node 依赖并启动项目（默认端口 3000）
5. 浏览器访问  http://localhost:3000  即可使用中药识别系统
 
二、接口地址说明
 
- 前端访问地址： http://localhost:3000 
- 后端 API 接口地址： http://localhost:5000/predict 
- 线上演示时，后端通过 ngrok 暴露为公网地址，前端会自动适配
 

📄 许可证
本项目仅供学习交流使用，禁止商用。