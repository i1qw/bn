import time
import requests
import logging
from threading import Thread
from datetime import datetime

# 配置日志（简化格式）
handler = logging.StreamHandler()
formatter = logging.Formatter('[时间同步] %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger('TimeSyncManager')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class TimeSyncManager:
    """时间同步管理器，用于同步本地时间与币安服务器时间"""
    
    def __init__(self, sync_interval=3600, max_allowed_offset=1500):
        """
        初始化时间同步管理器
        :param sync_interval: 同步间隔(秒)
        :param max_allowed_offset: 最大允许的时间偏移量(毫秒)
        """
        self.sync_interval = sync_interval  # 默认每小时同步一次
        self.max_allowed_offset = max_allowed_offset  # 默认最大允许1500ms偏移
        self.time_offset = 0  # 时间偏移量(毫秒)
        self.last_sync_time = 0  # 上次同步时间
        self.is_synced = False  # 是否已同步
        self.sync_thread = None  # 同步线程
        self.running = False  # 运行状态
    
    def start(self):
        """启动自动时间同步"""
        if self.running:
            return
            
        self.running = True
        # 立即进行一次同步
        self.sync_time()
        # 启动自动同步线程
        self.sync_thread = Thread(target=self._auto_sync)
        self.sync_thread.daemon = True
        self.sync_thread.start()
        # 不输出启动服务日志
    
    def stop(self):
        """停止自动时间同步"""
        self.running = False
        if self.sync_thread and self.sync_thread.is_alive():
            self.sync_thread.join(2.0)  # 等待线程结束，最多等待2秒
        # 不输出停止服务日志
    
    def _auto_sync(self):
        """自动同步时间的内部方法"""
        while self.running:
            try:
                time.sleep(self.sync_interval)
                self.sync_time()
            except Exception as e:
                logger.error(f"自动同步时间时发生错误: {str(e)}")
    
    def sync_time(self):
        """手动同步时间"""
        try:
            # 记录本地请求发送时间
            local_request_time = int(time.time() * 1000)
            
            # 请求币安服务器时间
            response = requests.get('https://api.binance.com/api/v3/time', timeout=10)
            response.raise_for_status()
            
            # 解析币安服务器时间
            binance_time = response.json().get('serverTime', 0)
            
            # 记录本地响应接收时间
            local_response_time = int(time.time() * 1000)
            
            # 计算网络延迟和时间偏移
            network_delay = (local_response_time - local_request_time) // 2
            self.time_offset = binance_time - local_response_time + network_delay
            self.last_sync_time = local_response_time
            
            # 检查时间偏移是否在允许范围内
            is_offset_acceptable = abs(self.time_offset) <= self.max_allowed_offset
            self.is_synced = True
            
            # 只输出一个表明同步成功的简洁日志
            if is_offset_acceptable:
                logger.info("时间戳同步成功")
            else:
                logger.info(f"时间戳同步成功 (注意: 时间偏移 {abs(self.time_offset)}ms 超过允许范围)")
                
        except requests.RequestException as e:
            logger.error(f"同步时间时发生网络错误: {str(e)}")
            self.is_synced = False
        except Exception as e:
            logger.error(f"同步时间时发生未知错误: {str(e)}")
            self.is_synced = False
    
    def get_synced_timestamp(self):
        """获取同步后的时间戳(毫秒)"""
        # 如果尚未同步，先进行同步
        if not self.is_synced:
            self.sync_time()
        
        # 检查上次同步是否超过一定时间，如果是则重新同步
        current_time = int(time.time() * 1000)
        if current_time - self.last_sync_time > self.sync_interval * 1000:
            logger.info("上次同步时间过长，重新同步")
            self.sync_time()
        
        # 返回同步后的时间戳
        return current_time + self.time_offset
    
    def get_synced_time(self):
        """获取同步后的时间(秒)"""
        return self.get_synced_timestamp() / 1000
    
    def _format_time(self, timestamp_ms):
        """格式化时间戳为可读时间"""
        try:
            return datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        except:
            return "Invalid time"

# 创建全局时间同步管理器实例
time_sync_manager = TimeSyncManager()

# 启动时间同步
time_sync_manager.start()