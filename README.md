Markdown
# 智能农场视觉监测与数据管理平台

## Description

本项目是一个基于 Django 的智能农场视觉监测与数据管理平台。系统提供设备、农田、监控数据和警告信息的后台管理界面，适用于农业物联网和环境监测场景。

## Installation

1. 克隆仓库并进入目录：
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/<your-repo>.git
   cd <your-repo>
创建并激活 Python 虚拟环境：

Bash
python -m venv .venv
source .venv/bin/activate
安装依赖：

Bash
pip install -r requirements.txt
Usage
执行数据库迁移：

Bash
python manage.py migrate
创建超级用户（可选）：

Bash
python manage.py createsuperuser
启动开发服务器：

Bash
python manage.py runserver 0.0.0.0:8000
在浏览器中访问：
http://127.0.0.1:8000

Project Structure
smartfarm_platform/：Django 项目设置和 URL 路由

monitoring/：应用模型、视图、管理后台和业务逻辑

templates/：Django 模板文件

static/：静态资源文件

manage.py：Django 管理命令入口

Notes
当前仓库为标准 Django 项目结构。

项目配置由 smartfarm_platform/settings.py 管理。

目前不依赖 config.py 或 config.yaml，无须额外配置模板文件。

生产部署时请设置 DEBUG=False 及合适的 ALLOWED_HOSTS。

Disclaimer
本项目代码已做脱敏处理，删除了个人服务器绝对路径和隐私配置。请勿将敏感数据、个人配置文件或私有文件提交到公共仓库。
