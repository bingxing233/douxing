// backend/utils/api_key_manager.py
import os
import yaml
from datetime import datetime, timedelta
from typing import Dict, Optional

class APIKeyManager:
    """API密钥管理器"""
    
    def __init__(self, config_file: str = "configs/recruitment_config.yml"):
        self.config_file = config_file
        self.keys = self._load_keys()
        self.access_logs = []
    
    def _load_keys(self) -> Dict[str, Dict]:
        """加载API密钥配置"""
        try:
            with open(self.config_file, "r") as f:
                config = yaml.safe_load(f)
            return config.get("api_keys", {})
        except Exception as e:
            print(f"加载API密钥配置失败: {e}")
            return {}
    
    def get_key(self, service: str) -> Optional[str]:
        """获取指定服务的API密钥"""
        key_info = self.keys.get(service)
        if not key_info:
            return None
        
        # 检查密钥是否过期
        if self._is_key_expired(key_info):
            print(f"API密钥 {service} 已过期")
            return None
        
        # 记录访问日志
        self._log_access(service)
        
        # 返回密钥值
        return key_info.get("value") or key_info.get("key")
    
    def _is_key_expired(self, key_info: Dict) -> bool:
        """检查密钥是否过期"""
        expiry_date = key_info.get("expiry_date")
        if not expiry_date:
            return False
        
        try:
            expiry = datetime.fromisoformat(expiry_date)
            return datetime.now() > expiry
        except Exception:
            return False
    
    def _log_access(self, service: str):
        """记录密钥访问日志"""
        log_entry = {
            "service": service,
            "timestamp": datetime.now().isoformat(),
            "ip_address": os.getenv("REMOTE_ADDR", "unknown")
        }
        self.access_logs.append(log_entry)
        
        # 限制日志数量
        if len(self.access_logs) > 1000:
            self.access_logs = self.access_logs[-500:]
    
    def rotate_key(self, service: str) -> bool:
        """轮换指定服务的API密钥"""
        # 这里应该实现实际的密钥轮换逻辑
        # 例如调用云服务提供商的API来生成新密钥
        print(f"模拟轮换 {service} 的API密钥")
        return True
    
    def check_key_usage(self, service: str) -> Dict:
        """检查密钥使用情况"""
        service_logs = [log for log in self.access_logs if log["service"] == service]
        
        return {
            "service": service,
            "total_requests": len(service_logs),
            "recent_requests": len([log for log in service_logs 
                                  if datetime.fromisoformat(log["timestamp"]) > datetime.now() - timedelta(hours=1)])
        }
    
    def validate_key_permissions(self, service: str, required_permissions: list) -> bool:
        """验证密钥权限"""
        key_info = self.keys.get(service)
        if not key_info:
            return False
        
        key_permissions = key_info.get("permissions", [])
        # 检查是否包含所有必需权限
        return all(perm in key_permissions for perm in required_permissions)