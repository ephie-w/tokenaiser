import os

from google.adk.agents import Agent
from google.adk.code_executors import VertexAiCodeExecutor
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool, ToolContext
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.genai import types
from . import tools
import logging
import os
from typing import Any, Dict, Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool, ToolContext
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.genai import types
from . import tools
ADK_BUILTIN_BQ_EXECUTE_SQL_TOOL = "execute_sql"
logger = logging.getLogger(__name__)

bigquery_tool_filter = [ADK_BUILTIN_BQ_EXECUTE_SQL_TOOL]
bigquery_tool_config = BigQueryToolConfig(
    write_mode=WriteMode.BLOCKED, application_name=''
)
bigquery_toolset = BigQueryToolset(
    tool_filter=bigquery_tool_filter, bigquery_tool_config=bigquery_tool_config
)
analytics_agent = Agent(
    model=os.getenv("ANALYTICS_AGENT_MODEL", ""),
    name="analytics_agent",
    instruction="You are an analyst agent responsible for analyzing data and providing insights.",
    code_executor=VertexAiCodeExecutor(
        optimize_data_file=True,
        stateful=True,
    ),
    tools=[
        bigquery_toolset,
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
