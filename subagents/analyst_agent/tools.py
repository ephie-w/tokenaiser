# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This file contains the tools used by the database agent (Mock version)."""

import datetime
import logging
import os
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

# Mock configuration - using environment variables with defaults
MAX_NUM_ROWS = 10000


def _serialize_value_for_sql(value):
    """Serializes a Python value from a pandas DataFrame into a BigQuery SQL literal."""
    if isinstance(value, (list, np.ndarray)):
        # Format arrays.
        return f"[{', '.join(_serialize_value_for_sql(v) for v in value)}]"
    if pd.isna(value):
        return "NULL"
    if isinstance(value, str):
        # Escape single quotes and backslashes for SQL strings.
        # NOTE: This will throw an exception in Python <= 3.11 because
        # Python 3.12 introduces better f-string handling.
        new_value = value.replace("\\", "\\\\").replace("'", "''")
        return f"'{new_value}'"
    if isinstance(value, bytes):
        decoded = value.decode("utf-8", "replace")
        new_value = decoded.replace("\\", "\\\\").replace("'", "''")
        return f"b'{new_value}'"
    if isinstance(value, (datetime.datetime, datetime.date, pd.Timestamp)):
        # Timestamps and datetimes need to be quoted.
        return f"'{value}'"
    if isinstance(value, dict):
        # For STRUCT, BQ expects ('val1', 'val2', ...).
        # The values() order from the dataframe should match the column order.
        string_values = [_serialize_value_for_sql(v) for v in value.values()]
        return f"({", ".join(string_values)})"
    return str(value)


# Mock database settings
database_settings = {
    "bigquery": {
        "schema": {
            "mock_project.mock_dataset.mock_table": {
                "table_schema": [
                    ("id", "INTEGER"),
                    ("name", "STRING"),
                    ("value", "FLOAT"),
                    ("created_at", "TIMESTAMP"),
                ],
                "example_values": {},
            }
        }
    }
}


def bigquery_nl2sql(
    question: str,
    tool_context: ToolContext,
) -> str:
    """Generates a SQL query from a natural language question (Mock version).

    Args:
        question (str): Natural language question.
        tool_context (ToolContext): The tool context to use for generating the
            SQL query.

    Returns:
        str: An SQL statement to answer this question.
    """
    logger.debug("bigquery_nl2sql (mock) - question: %s", question)

    # Initialize database_settings in tool_context if not present
    if "database_settings" not in tool_context.state:
        tool_context.state["database_settings"] = database_settings

    # Mock SQL generation - simple pattern matching
    question_lower = question.lower()
    
    # Simple mock SQL based on question keywords
    if "count" in question_lower or "how many" in question_lower:
        sql = "SELECT COUNT(*) as count FROM `mock_project.mock_dataset.mock_table`"
    elif "sum" in question_lower or "total" in question_lower:
        sql = "SELECT SUM(value) as total FROM `mock_project.mock_dataset.mock_table`"
    elif "average" in question_lower or "avg" in question_lower or "mean" in question_lower:
        sql = "SELECT AVG(value) as average FROM `mock_project.mock_dataset.mock_table`"
    elif "select" in question_lower and "all" in question_lower:
        sql = "SELECT * FROM `mock_project.mock_dataset.mock_table` LIMIT 100"
    else:
        # Default mock SQL
        sql = "SELECT id, name, value FROM `mock_project.mock_dataset.mock_table` LIMIT 10"

    logger.debug("bigquery_nl2sql (mock) - sql:\n%s", sql)

    # Store SQL in tool context
    tool_context.state["sql_query"] = sql

    return sql


def get_insights(
    sql_query: str,
    tool_context: ToolContext,
) -> Dict[str, Any]:
    """Generates insights from SQL query results (Mock version).

    Args:
        sql_query (str): SQL query to analyze.
        tool_context (ToolContext): The tool context.

    Returns:
        Dict[str, Any]: Insights dictionary containing analysis results.
    """
    logger.debug("get_insights (mock) - sql_query: %s", sql_query)

    # Mock insights based on SQL query
    insights = {
        "summary": "Mock insights generated from SQL query",
        "key_findings": [
            "This is a mock insight 1",
            "This is a mock insight 2",
            "This is a mock insight 3",
        ],
        "recommendations": [
            "Mock recommendation 1",
            "Mock recommendation 2",
        ],
        "data_points": {
            "total_records": 100,
            "date_range": "2024-01-01 to 2024-12-31",
        },
    }

    # Store insights in tool context
    if "insights" not in tool_context.state:
        tool_context.state["insights"] = []
    tool_context.state["insights"].append(insights)

    logger.debug("get_insights (mock) - insights: %s", insights)

    return insights


# Mock BigQuery tools
def bq_list_datasets(
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Lists all datasets in a BigQuery project (Mock version)."""
    logger.debug("bq_list_datasets (mock) - project_id: %s", project_id)
    return [
        {
            "dataset_id": "mock_dataset",
            "project_id": project_id or "mock_project",
            "location": "US",
        }
    ]


def bq_list_tables(
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Lists all tables in a BigQuery dataset (Mock version)."""
    logger.debug("bq_list_tables (mock) - dataset_id: %s, project_id: %s", dataset_id, project_id)
    return [
        {
            "table_id": "mock_table",
            "dataset_id": dataset_id,
            "project_id": project_id or "mock_project",
            "type": "TABLE",
        }
    ]


def bq_get_dataset_info(
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets information about a BigQuery dataset (Mock version)."""
    logger.debug("bq_get_dataset_info (mock) - dataset_id: %s, project_id: %s", dataset_id, project_id)
    return {
        "dataset_id": dataset_id,
        "project_id": project_id or "mock_project",
        "location": "US",
        "description": f"Mock dataset: {dataset_id}",
    }


def bq_get_table_info(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets information about a BigQuery table (Mock version)."""
    logger.debug("bq_get_table_info (mock) - table_id: %s, dataset_id: %s", table_id, dataset_id)
    return {
        "table_id": table_id,
        "dataset_id": dataset_id,
        "project_id": project_id or "mock_project",
        "type": "TABLE",
        "num_rows": 1000,
        "num_bytes": 1024000,
    }


def bq_get_table_schema(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Gets the schema of a BigQuery table (Mock version)."""
    logger.debug("bq_get_table_schema (mock) - table_id: %s, dataset_id: %s", table_id, dataset_id)
    return [
        {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
        {"name": "name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "value", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    ]


def bq_get_table_data(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    max_results: int = 10,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Gets sample data from a BigQuery table (Mock version)."""
    logger.debug("bq_get_table_data (mock) - table_id: %s, dataset_id: %s, max_results: %s", 
                 table_id, dataset_id, max_results)
    return [
        {"id": 1, "name": "Item 1", "value": 10.5, "created_at": "2024-01-01T00:00:00Z"},
        {"id": 2, "name": "Item 2", "value": 20.3, "created_at": "2024-01-02T00:00:00Z"},
    ][:max_results]


def bq_get_table_metadata(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets metadata about a BigQuery table (Mock version)."""
    logger.debug("bq_get_table_metadata (mock) - table_id: %s, dataset_id: %s", table_id, dataset_id)
    return {
        "table_id": table_id,
        "dataset_id": dataset_id,
        "project_id": project_id or "mock_project",
        "type": "TABLE",
        "num_rows": 1000,
        "num_bytes": 1024000,
        "description": f"Mock table metadata for {table_id}",
    }


def bq_get_table_statistics(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets statistics about a BigQuery table (Mock version)."""
    logger.debug("bq_get_table_statistics (mock) - table_id: %s, dataset_id: %s", table_id, dataset_id)
    return {
        "table_id": table_id,
        "num_rows": 1000,
        "num_bytes": 1024000,
        "last_modified_time": "2024-01-01T00:00:00Z",
    }


def bq_get_table_partitions(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Gets partition information for a BigQuery table (Mock version)."""
    logger.debug("bq_get_table_partitions (mock) - table_id: %s, dataset_id: %s", table_id, dataset_id)
    return [
        {
            "partition_id": "20240101",
            "num_rows": 100,
            "num_bytes": 102400,
        }
    ]
