// backend/utils/data_security.py
from cryptography.fernet import Fernet
import os
import base64
from datetime import datetime, timedelta
import hashlib

class DataSecurity:
    """数据安全和隐私保护工具"""
    
    def __init__(self):
        # 从环境变量获取加密密钥，如果不存在则生成
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_key(self):
        """获取或创建加密密钥"""
        key = os.getenv("ENCRYPTION_KEY")
        if key:
            # 确保密钥是base64编码的32字节
            return base64.urlsafe_b64encode(key.encode().ljust(32)[:32])
        else:
            # 生成新的密钥
            return Fernet.generate_key()
    
    def encrypt_resume(self, resume_text: str) -> str:
        """加密简历内容"""
        encrypted_data = self.cipher.encrypt(resume_text.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_resume(self, encrypted_resume: str) -> str:
        """解密简历内容"""
        encrypted_data = base64.urlsafe_b64decode(encrypted_resume.encode())
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode()
    
    def hash_candidate_info(self, candidate_info: dict) -> str:
        """对候选人信息进行哈希处理，用于匿名化"""
        # 将字典转换为字符串并排序以确保一致性
        info_str = str(sorted(candidate_info.items()))
        return hashlib.sha256(info_str.encode()).hexdigest()
    
    def should_delete_resume(self, upload_date: datetime, retention_days: int = 30) -> bool:
        """检查简历是否应该被删除"""
        retention_date = upload_date + timedelta(days=retention_days)
        return datetime.now() > retention_date
    
    def mask_sensitive_info(self, text: str) -> str:
        """遮蔽敏感信息（如手机号、邮箱等）"""
        import re
        
        # 遮蔽手机号
        text = re.sub(r'1[3-9]\d{9}', '1**********', text)
        
        # 遮蔽邮箱
        text = re.sub(r'[\w\.-]+@[\w\.-]+', '***@***.***', text)
        
        # 遮蔽身份证号
        text = re.sub(r'\d{17}[\dXx]', '******************', text)
        
        return text