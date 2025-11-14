from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from subagents.analyst_agent import analyst_agent
root_agent = Agent(
    name="bq-analyst",
    model="gemini-2.0-flash",
    description="Data Science Agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    - stock_analyst
    - funny_nerd

    You also have access to the following tools:
    - news_analyst
    - get_current_time
    """,
    sub_agents=[analyst_agent],
    tools=[],
)
