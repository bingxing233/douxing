// backend/plugins/plugin_manager.py
import os
import importlib
from typing import Dict, Any, List
import yaml

class PluginManager:
    """插件管理器"""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.plugins = {}
        self.loaded_plugins = {}
    
    def discover_plugins(self) -> List[str]:
        """发现可用插件"""
        plugins = []
        if os.path.exists(self.plugins_dir):
            for item in os.listdir(self.plugins_dir):
                item_path = os.path.join(self.plugins_dir, item)
                if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "__init__.py")):
                    plugins.append(item)
        return plugins
    
    def load_plugin(self, plugin_name: str) -> bool:
        """加载插件"""
        try:
            plugin_module = importlib.import_module(f"plugins.{plugin_name}")
            if hasattr(plugin_module, "Plugin"):
                plugin_instance = plugin_module.Plugin()
                self.loaded_plugins[plugin_name] = plugin_instance
                print(f"成功加载插件: {plugin_name}")
                return True
            else:
                print(f"插件 {plugin_name} 缺少Plugin类")
                return False
        except Exception as e:
            print(f"加载插件 {plugin_name} 失败: {e}")
            return False
    
    def load_all_plugins(self):
        """加载所有插件"""
        available_plugins = self.discover_plugins()
        for plugin_name in available_plugins:
            self.load_plugin(plugin_name)
    
    def get_plugin(self, plugin_name: str):
        """获取插件实例"""
        return self.loaded_plugins.get(plugin_name)
    
    def execute_plugin_method(self, plugin_name: str, method_name: str, *args, **kwargs):
        """执行插件方法"""
        plugin = self.get_plugin(plugin_name)
        if plugin and hasattr(plugin, method_name):
            method = getattr(plugin, method_name)
            return method(*args, **kwargs)
        else:
            raise ValueError(f"插件 {plugin_name} 不存在方法 {method_name}")

# 基础插件类
class BasePlugin:
    """基础插件类"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.description = "基础插件类"
    
    def initialize(self):
        """初始化插件"""
        pass
    
    def cleanup(self):
        """清理插件"""
        pass