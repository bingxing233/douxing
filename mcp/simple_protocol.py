// mcp/simple_protocol.py
class SimpleMCP:
    """简化版MCP协议，仅实现基础通信"""
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.agents = {}  # 存储已注册的智能体
    
    def register_agent(self, agent):
        """注册智能体"""
        self.agents[agent.agent_id] = agent
    
    def send_message(self, target_agent_id, action, data):
        """发送消息给目标智能体"""
        if target_agent_id not in self.agents:
            raise ValueError(f"智能体{target_agent_id}未注册")
        
        target_agent = self.agents[target_agent_id]
        return target_agent.handle_message(action, data)