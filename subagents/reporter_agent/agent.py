'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-14 15:53:12
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2025-11-14 16:07:00
FilePath: /tokenaiser/subagents/reporter_agent/agent.py
Description: 
'''
from google.adk.agents import Agent
from . import tools

from .prompts import return_instructions_reporter


reporter_agent = Agent(
    name="reporter_agent",
    model="gemini-2.5-pro",
    description="An agent that dispatches notifications to different channels.",
    instruction=return_instructions_reporter(),
    tools=[
        tools.generate_reporter
    ],
)#dummy
