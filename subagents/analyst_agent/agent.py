'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-14 14:06:39
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2025-11-14 14:45:01
FilePath: /tokenaiser/subagents/analyst_agent/agent.py
Description: 
'''
import os
import logging

from google.adk.agents import Agent
from google.adk.code_executors import VertexAiCodeExecutor
from google.adk.tools.bigquery import BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode
from google.genai import types
from . import tools
ADK_BUILTIN_BQ_EXECUTE_SQL_TOOL = "execute_sql"
logger = logging.getLogger(__name__)
analyst_agent = Agent(
    model=os.getenv("ANALYTICS_AGENT_MODEL", ""),
    name="analytics_agent",
    instruction="You are an analyst agent responsible for analyzing data and providing insights.",
    tools=[
        tools.bq_get_table_info,
        tools.bq_get_dataset_info,
        tools.bq_list_tables,
        tools.bq_list_datasets,
        tools.bq_get_table_schema,
        tools.bq_get_table_data,
        tools.bq_get_table_metadata,
        tools.bq_get_table_statistics,
        tools.bq_get_table_partitions,
        tools.bigquery_nl2sql,
        tools.get_insights
    ],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
