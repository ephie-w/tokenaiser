from google.adk.agents import Agent

from .prompts import return_instructions_reporter

reporter_agent = Agent(
    name="reporter_agent",
    model="gemini-2.5-pro",
    description="An agent that dispatches notifications to different channels.",
    instruction=return_instructions_reporter(),
    tools=[
        tools.dispatch_consumer,
        tools.dispatch_editorial,
        tools.apihub
    ],
)#dummy
