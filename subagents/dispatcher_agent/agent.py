'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-14 14:59:06
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2025-11-14 15:31:09
FilePath: /tokenaiser/subagents/dispatcher_agent/agent.py
Description: 
'''
from google.adk.agents import Agent

from .prompts import return_instructions_dispatcher
from . import tools

# Create the dispatcher agent
dispatcher_agent = Agent(
    name="dispatcher_agent",
    model="gemini-2.5-pro",
    description="An agent that dispatches notifications to different channels.",
    instruction=return_instructions_dispatcher(),
    tools=[
        tools.dispatch_consumer,
        tools.dispatch_editorial,
        tools.apihub
    ],
)
