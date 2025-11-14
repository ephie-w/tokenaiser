from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .subagents.analyst_agent.agent import analytics_agent
from .subagents.dispatcher_agent.agent import dispatcher_agent
# from .subagents.reporter_agent.agent import reporter_agent
from .prompts import return_instructions_root


# Create sequential agent that executes analyst_agent first, then dispatcher_agent
sequential_agent = Agent(
    name="sequential_agent",
    model="gemini-2.5-pro",
    description="Sequential agent that executes analyst_agent then dispatcher_agent",
    instruction="""
    You are a sequential orchestrator agent. Your task is to execute agents in a specific order:
    
    STEP 1: First, you MUST call the analytics_agent tool.
    STEP 2: After analytics_agent completes, you MUST call the dispatcher_agent tool.
    IMPORTANT: You must execute these agents sequentially - analytics_agent first, then dispatcher_agent.
    Do not call dispatcher_agent until analytics_agent has finished.
    """,
    sub_agents=[analytics_agent, dispatcher_agent],
    tools=[
        AgentTool(analytics_agent),
        AgentTool(dispatcher_agent),
    ],
)

# Keep root_agent for backward compatibility
root_agent = sequential_agent