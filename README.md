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

1. 复制配置模板：
   ```bash
cp config.yaml.example config.yaml
```
2. 编辑 `config.yaml`，将其中的占位路径替换成你的本地目录，例如：
   - `dataset_root: ./BCCD`
   - `data_yaml: ./datasets/data.yaml`
   - `model_path: ./yolov8n.pt`
   - `output_dir: ./runs`
   - `log_dir: ./logs`
3. 运行 Django 开发服务器：
   ```bash
python manage.py runserver 0.0.0.0:8000
```
4. 如果你使用 `app_gradio.py` 启动 Gradio 接口：
   ```bash
python app_gradio.py
```

## Configuration

本仓库提供 `config.py` 和 `config.yaml.example`，用于将本地路径和运行参数从代码中抽离出来。建议：

- 不要将 `config.yaml` 提交到仓库。
- 通过 `.gitignore` 自动忽略本地配置文件和私有数据。

### 推荐的配置字段

- `project_root`: 项目根目录
- `dataset_root`: 原始数据目录
- `data_yaml`: 数据集 YAML 配置文件路径
- `model_path`: 模型权重文件路径
- `output_dir`: 训练或推理结果输出目录
- `log_dir`: 日志目录
- `device`: 运行设备（如 `cpu` 或 `cuda`）
- `gradio_port`: Gradio 服务端口
- `secret_key`: Django 或其他服务密钥
- `debug`: 是否启用调试模式
- `allowed_hosts`: 允许的主机列表

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
