from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from .prompts import return_instructions_dispatcher


def dispatch_consumer(tool_context: ToolContext) -> dict:
    """Invoke API to dispatch notification to consumer channel."""
    

    return {"status": "success", "dispatch_event": "Subscriptions have dipped by %10 against daily average"}

def dispatch_editorial(tool_content: ToolContext) -> dict:
    """Invoke API to dispatch notification to editorial channel."""

    return {"status": "success", "dispatch_event": "COnversion rate has decreased by 20%"}

# Create the funny nerd agent
dispatcher_agent = Agent(
    name="dispatcher_agent",
    model="gemini-2.5-pro",
    description="An agent that tells nerdy jokes about various topics.",
    instruction=return_instructions_dispatcher(),
    tools=[dispatch_consumer,dispatch_editorial],
)
