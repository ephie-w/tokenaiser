from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.base_agent import Tool  # 如果有工具的话

# 创建子 Agent 的配置路径
sub_agents = [
    {
        "config_path": "./taskParse.yaml"
    }
]

# 根 Agent 的 instruction
instruction = """
You are the root orchestrator agent responsible for understanding
user requests and routing them to the correct sub-agent. 
- If the user request involves data management, cleaning, or integration, flow_type is dataflow. 
- If the request involves document processing or robotic automation, flow_type is praflow.

Please think about this question step by step before providing the final answer. 
Put the thinking process within the <thought> </thought> tags.

Call the taskParse sub-agent the flow_request in the following format:
{
    "flow_type": "dataflow" | "praflow", 
    "user_request": "user request"
}
"""

# 创建 Agent
tokenAIsers = LlmAgent(
    name="tokenAIsers",
    model="gemini-2.5-flash",
    agent_class="LlmAgent",
    instruction=instruction,
    sub_agents=sub_agents,
    tools=[],        # 如果你有工具可以放在这里
    output_key="flow_request"
)
