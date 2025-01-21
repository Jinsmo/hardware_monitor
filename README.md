我来帮您创建一个 README.md 文件：

# 服务器硬件监控系统

## 简介
一个基于 Python Flask 开发的轻量级服务器硬件监控系统，提供 RESTful API 接口，用于实时监控服务器的 CPU、内存、网络和磁盘使用情况。

## 功能特点
- 实时监控 CPU 使用率和核心信息
- 内存使用状况监控
- 网络流量统计
- 磁盘 I/O 和使用情况监控
- 基于 Basic Auth 的安全认证
- 支持跨域请求
- 完整的日志记录
- 可配置的服务器参数

## 目录结构
```bash
hardware_monitor/
├── app.py              # 主应用程序
├── config.py           # 配置文件
├── config.template.py  # 配置文件模板
├── requirements.txt    # 依赖包列表
├── start.sh           # 启动脚本
├── README.md          # 项目说明文档
└── .gitignore         # Git忽略文件
```

## 快速开始

### 1. 环境要求
- Python 3.6+
- pip 包管理工具

### 2. 安装步骤
```bash
# 克隆项目
git clone https://github.com/your-username/hardware-monitor.git
cd hardware-monitor

# 创建并激活虚拟环境
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置
cp config.template.py config.py
# 根据需要修改 config.py 中的配置
```

### 3. 运行服务
```bash
# 方式1：使用启动脚本
chmod +x start.sh
./start.sh

# 方式2：直接运行
python app.py
```

## API 使用示例

### 1. 检查服务状态
```bash
curl http://localhost:5000/
```

### 2. 获取硬件信息
```bash
curl -u admin:your_password http://localhost:5000/api/hardware/status
```

### 3. Python 客户端示例
```python
import requests
from requests.auth import HTTPBasicAuth

def get_hardware_status(host='localhost', port=5000, username='admin', password='your_password'):
    """获取服务器硬件状态"""
    url = f'http://{host}:{port}/api/hardware/status'
    try:
        response = requests.get(
            url, 
            auth=HTTPBasicAuth(username, password),
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == '__main__':
    status = get_hardware_status()
    if status:
        print(f"CPU使用率: {status['cpu']['usage']['total_usage']}%")
        print(f"内存使用率: {status['memory']['percentage']}%")
```

## 配置说明

### 主要配置项
配置文件 `config.py` 包含以下配置：

1. 认证配置
```python
AUTH_CONFIG = {
    'USERS': {
        'admin': 'your_password'  # 修改默认密码
    }
}
```

2. 服务器配置
```python
SERVER_CONFIG = {
    'HOST': '0.0.0.0',  # 监听地址
    'PORT': 5000,       # 监听端口
    'DEBUG': False      # 调试模式
}
```

3. 日志配置
```python
LOG_CONFIG = {
    'LEVEL': 'INFO',    # 日志级别
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
```

## 安全建议

### 1. 基本安全配置
- 修改默认密码
- 使用 HTTPS
- 配置防火墙规则
- 限制访问IP

### 2. 生产环境部署
- 使用反向代理（如 Nginx）
- 设置适当的文件权限
- 使用非 root 用户运行
- 启用 HTTPS

## 常见问题

### 1. 认证失败
- 检查用户名密码是否正确
- 确认认证头格式是否正确
- 查看日志中的具体错误信息

### 2. 性能问题
- 建议请求间隔不少于1秒
- 避免频繁请求磁盘IO信息
- 根据需要调整日志级别

## 维护建议

### 1. 日常维护
- 定期检查日志文件
- 监控服务运行状态
- 及时更新依赖包

### 2. 性能优化
- 适当调整请求频率
- 根据需要缓存数据
- 优化日志记录

## 贡献指南
1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证
MIT License

## 作者
[您的名字]

## 联系方式
- GitHub: [@Jinsmo](https://github.com/Jinsmo)
- QQ群：976416084

这个 README.md：
1. 提供了简洁的项目介绍
2. 包含了完整的安装和使用说明
3. 提供了实用的示例代码
4. 包含了重要的配置说明
5. 添加了安全建议和维护建议
6. 保持了清晰的结构和格式
7. 适合作为项目的首页文档

需要添加或修改其他内容吗？
