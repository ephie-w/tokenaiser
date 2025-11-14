from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .subagents.analyst_agent.agent import analyst_agent
# from .subagents.dispatcher_agent.agent import dispatcher_agent
# from .subagents.reporter_agent.agent import reporter_agent
from .prompts import return_instructions_root


root_agent = Agent(
    name="bq_analyst",
    model="gemini-2.5-pro",
    description="Data Science Agent",
    instruction=return_instructions_root(),
   # sub_agents=[analyst_agent, dispatcher_agent, reporter_agent],
    sub_agents=[analyst_agent],
    tools=[
    ],
)