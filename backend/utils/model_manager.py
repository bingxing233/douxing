// backend/utils/model_manager.py
from typing import Dict, Any, Optional
import os
import yaml
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """基础模型接口"""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        pass

class ModelManager:
    """模型管理器，支持多种AI模型的插拔式切换"""
    
    def __init__(self, config_file: str = "configs/recruitment_config.yml"):
        self.config_file = config_file
        self.models = {}
        self.active_model = None
        self._load_config()
        self._initialize_models()
    
    def _load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_file, "r") as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.config = {}
    
    def _initialize_models(self):
        """初始化所有配置的模型"""
        model_configs = self.config.get("models", {})
        
        # 初始化Qwen模型
        if "qwen" in model_configs:
            self.models["qwen"] = self._create_qwen_model(model_configs["qwen"])
        
        # 初始化其他模型（如需要）
        # 可以在这里添加对其他模型的支持
        
        # 设置默认激活模型
        default_model = self.config.get("models", {}).get("default_model", "qwen")
        if default_model in self.models:
            self.active_model = self.models[default_model]
    
    def _create_qwen_model(self, config: Dict[str, Any]):
        """创建Qwen模型实例"""
        try:
            from nemo_agent.llms import OpenAICompatible
            qwen_api_key = os.getenv("QWEN_API_KEY")
            
            return OpenAICompatible(
                model_name=config["model_name"],
                base_url=config["base_url"],
                api_key=qwen_api_key,
                temperature=config.get("temperature", 0.7),
                max_tokens=config.get("max_tokens", 2048)
            )
        except Exception as e:
            print(f"创建Qwen模型失败: {e}")
            return None
    
    def switch_model(self, model_name: str) -> bool:
        """切换当前使用的模型"""
        if model_name in self.models and self.models[model_name]:
            self.active_model = self.models[model_name]
            print(f"已切换到模型: {model_name}")
            return True
        else:
            print(f"模型 {model_name} 不存在或未正确初始化")
            return False
    
    def generate(self, prompt: str, model_name: Optional[str] = None, **kwargs) -> str:
        """使用指定模型生成文本"""
        model = self.active_model
        if model_name and model_name in self.models:
            model = self.models[model_name]
        
        if not model:
            raise ValueError("没有可用的模型")
        
        return model.generate(prompt=prompt, **kwargs)
    
    def get_available_models(self) -> list:
        """获取可用模型列表"""
        return [name for name, model in self.models.items() if model is not None]
    
    def get_active_model_info(self) -> Dict[str, Any]:
        """获取当前激活模型的信息"""
        if self.active_model and hasattr(self.active_model, "get_model_info"):
            return self.active_model.get_model_info()
        return {"name": "unknown", "info": "无法获取模型信息"}