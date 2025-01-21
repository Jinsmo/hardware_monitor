"""
配置文件模板
实际使用时复制为 config.py 并修改相关配置
"""

# 认证配置
AUTH_CONFIG = {
    'USERS': {
        'admin': 'change_this_password'  # 修改这个默认密码
    }
}

# 服务器配置
SERVER_CONFIG = {
    'HOST': '0.0.0.0',  # 监听所有网络接口
    'PORT': 5000,       # 服务端口
    'DEBUG': False      # 生产环境禁用调试模式
}

# 日志配置
LOG_CONFIG = {
    'LEVEL': 'INFO',    # 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# API配置
API_CONFIG = {
    'VERSION': 'v1',
    'PREFIX': '/api'
} 