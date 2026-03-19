# 🏰 汉诺塔游戏 - 超级玛丽主题

一个基于 Flask 的汉诺塔可视化 Web 应用，采用超级玛丽游戏风格设计。

## 功能特点

- 🎮 **可视化演示**：实时展示汉诺塔的解决过程
- 🎨 **超级玛丽主题**：经典游戏风格的界面设计
- 🎵 **音效系统**：移动圆盘和完成游戏的音效
- ⚡ **多种速度**：支持慢、中、快三种播放速度
- 🎯 **双模式**：自动模式和手动模式
- 📱 **响应式设计**：支持移动端访问

## 技术栈

- **后端**：Python Flask
- **前端**：HTML5, CSS3, JavaScript
- **样式**：超级玛丽像素风格

## 快速开始

### 安装依赖

```bash
pip install flask flask-cors
```

### 运行服务器

```bash
python hanoi_server.py
```

服务器将在 `http://localhost:5001` 启动。

## 项目结构

```
├── hanoi.py              # 汉诺塔算法实现
├── hanoi_server.py       # Flask 后端服务器
├── test_hanoi.py         # 算法单元测试
├── test_hanoi_server.py  # API 测试
├── static/
│   ├── index.html        # 主页面
│   ├── app.js            # 前端逻辑
│   └── style.css         # 样式文件
```

## 许可证

MIT License