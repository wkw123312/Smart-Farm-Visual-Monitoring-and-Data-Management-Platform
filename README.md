# 智能农场视觉监测与数据管理平台

## Description

本项目是一个面向智能农业场景的视觉监测与数据管理平台。它基于 Django 构建后台管理系统，支持设备、农田、检测和告警数据的可视化展示。项目采用配置文件化方式管理本地数据路径、模型路径和运行参数，避免在源代码中写死个人服务器路径。

## Installation

1. 克隆仓库并进入目录：
   ```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```
2. 创建并激活 Python 虚拟环境：
   ```bash
python -m venv .venv
source .venv/bin/activate
```
3. 安装依赖：
   ```bash
pip install -r requirements.txt
```

## Usage

1. 运行 Django 开发服务器：
   ```bash
python manage.py runserver 0.0.0.0:8000
```

2. 在浏览器中访问：
   ```bash
http://127.0.0.1:8000
```

## Configuration

本项目是一个 Django Web 应用，配置主要由 `smartfarm_platform/settings.py` 管理。

如果你需要扩展本项目，可以在未来通过 `config.yaml` 或环境变量注入配置，但当前代码并不依赖 `config.py`。
## Disclaimer

本项目代码已做脱敏处理，删除了个人服务器绝对路径和隐私配置。使用前请务必创建并编辑 `config.yaml`，将所有路径改为你本地的合法目录。请勿将包含敏感信息的配置文件、模型权重或私有数据提交到公共仓库。

## Git 操作

```bash
git init
git add .
git commit -m "Initial project import with sanitized config templates and docs"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```
