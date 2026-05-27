# 智能农场视觉监测与数据管理平台

## Description

本项目是一个基于 Django 的智能农场视觉监测与数据管理平台。系统提供设备、农田、监控数据和告警信息的后台管理界面，适用于农业物联网和环境监测场景。

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

1. 执行数据库迁移：

```bash
python manage.py migrate
```

2. 创建超级用户（可选）：

```bash
python manage.py createsuperuser
```

3. 启动开发服务器：

```bash
python manage.py runserver 0.0.0.0:8000
```

4. 在浏览器中访问：

```bash
http://127.0.0.1:8000
```

## Project Structure

- `smartfarm_platform/`：Django 项目设置和 URL 路由
- `monitoring/`：应用模型、视图、管理后台和业务逻辑
- `templates/`：Django 模板文件
- `static/`：静态资源文件
- `manage.py`：Django 管理命令入口

## 页面展示
<img width="1877" height="917" alt="监控总览界面" src="https://github.com/user-attachments/assets/ea59fa79-3a3a-491c-b6e9-2d43f8f0e712" />
<img width="1898" height="597" alt="bed1fe955fd5230ead6530ba7798d45" src="https://github.com/user-attachments/assets/fe4d0a3a-b60a-443a-8fab-939a4c95f366" />



## Notes

- 当前仓库为标准 Django 项目结构。
- 项目配置由 `smartfarm_platform/settings.py` 管理。
- 当前代码不依赖 `config.py` 或 `config.yaml`。
- 生产部署时请设置 `DEBUG=False` 及合适的 `ALLOWED_HOSTS`。

## Disclaimer

本项目代码已做脱敏处理，删除了个人服务器绝对路径和隐私配置。请勿将敏感数据、个人配置文件或私有文件提交到公共仓库。


