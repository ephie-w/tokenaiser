from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .subagents.analyst_agent.agent import analyst_agent
from .subagents.dispatcher_agent.agent import dispatcher_agent
from .subagents.executive_agent.agent import reporter_agent
from .prompts import return_instructions_root
#from .tools.tools import get_current_time

root_agent = Agent(
    name="bq-analyst",
    model="gemini-2.5-pro",
    description="Data Science Agent",
    instruction=return_instructions_root(),
    sub_agents=[analyst_agent, dispatcher_agent, executive_agent],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
