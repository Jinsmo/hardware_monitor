"""
服务器硬件监控API
提供CPU、内存、网络和磁盘I/O等硬件信息的REST API接口
"""

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import psutil
import platform
import logging
import base64
from flask_cors import CORS
from config import AUTH_CONFIG, SERVER_CONFIG, LOG_CONFIG, API_CONFIG

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['LEVEL']),
    format=LOG_CONFIG['FORMAT']
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    """
    验证用户名和密码
    
    Args:
        username: 用户名
        password: 密码
        
    Returns:
        str or None: 验证成功返回用户名，失败返回None
    """
    try:
        users = AUTH_CONFIG['USERS']
        if username in users and users[username] == password:
            logger.info(f"Successful login for user: {username}")
            return username
        logger.warning(f"Invalid login attempt for user: {username}")
        return None
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None

# 添加一个简单的测试路由
@app.route('/', methods=['GET'])
def index():
    """测试服务器是否正常运行"""
    return jsonify({"message": "Server is running", "status": "OK"})

@app.route('/api/hardware/status', methods=['GET'])
@auth.login_required
def get_hardware_status():
    """
    获取所有硬件信息的统一接口
    返回CPU、内存、网络和磁盘的综合信息
    """
    try:
        # CPU信息
        cpu_info = {
            'model': platform.processor(),
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'usage': {
                'total_usage': psutil.cpu_percent(interval=1),
                'per_core': psutil.cpu_percent(interval=1, percpu=True)
            }
        }

        # 内存信息
        memory = psutil.virtual_memory()
        memory_info = {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percentage': memory.percent,
            'formatted': {
                'total': f"{memory.total / (1024**3):.2f} GB",
                'available': f"{memory.available / (1024**3):.2f} GB",
                'used': f"{memory.used / (1024**3):.2f} GB"
            }
        }

        # 网络信息
        network = psutil.net_io_counters()
        network_info = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv,
            'formatted': {
                'bytes_sent': f"{network.bytes_sent / (1024**2):.2f} MB",
                'bytes_recv': f"{network.bytes_recv / (1024**2):.2f} MB"
            }
        }

        # 磁盘I/O信息
        disk_io = psutil.disk_io_counters()
        disk_info = {
            'read_bytes': disk_io.read_bytes,
            'write_bytes': disk_io.write_bytes,
            'read_count': disk_io.read_count,
            'write_count': disk_io.write_count,
            'formatted': {
                'read': f"{disk_io.read_bytes / (1024**3):.2f} GB",
                'write': f"{disk_io.write_bytes / (1024**3):.2f} GB"
            }
        }

        # 磁盘使用情况
        disk_partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_partitions.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percentage': usage.percent,
                    'formatted': {
                        'total': f"{usage.total / (1024**3):.2f} GB",
                        'used': f"{usage.used / (1024**3):.2f} GB",
                        'free': f"{usage.free / (1024**3):.2f} GB"
                    }
                })
            except Exception as e:
                logger.warning(f"Could not get disk usage for {partition.mountpoint}: {str(e)}")

        # 整合所有信息
        hardware_status = {
            'cpu': cpu_info,
            'memory': memory_info,
            'network': network_info,
            'disk_io': disk_info,
            'disk_partitions': disk_partitions,
            'system_info': {
                'system': platform.system(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor()
            }
        }

        return jsonify(hardware_status)

    except Exception as e:
        logger.error(f"Error getting hardware status: {str(e)}")
        return jsonify({'error': 'Failed to get hardware status', 'message': str(e)}), 500

@app.before_request
def log_request_info():
    """记录请求信息用于调试"""
    logger.info('Headers: %s', request.headers)
    logger.info('Authorization: %s', request.headers.get('Authorization'))

if __name__ == '__main__':
    app.run(
        host=SERVER_CONFIG['HOST'],
        port=SERVER_CONFIG['PORT'],
        debug=SERVER_CONFIG['DEBUG']
    ) 