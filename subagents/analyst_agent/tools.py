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
MOCK_PROJECT_ID = "mock_project"
MOCK_DATASET_ID = "mock_dataset"
MOCK_TABLE_ID = "mock_table"
MOCK_FULL_TABLE_NAME = f"{MOCK_PROJECT_ID}.{MOCK_DATASET_ID}.{MOCK_TABLE_ID}"

database_settings = {
    "bigquery": {
        "schema": {
            MOCK_FULL_TABLE_NAME: {
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
    print(f"[MOCK] bigquery_nl2sql called with question: {question}")

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
    print(f"[MOCK] bigquery_nl2sql generated SQL: {sql}")

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
    print(f"[MOCK] get_insights called with sql_query: {sql_query}")

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
    print(f"[MOCK] get_insights returning insights:")
    print(f"  Summary: {insights['summary']}")
    print(f"  Key findings: {len(insights['key_findings'])} items")
    print(f"  Recommendations: {len(insights['recommendations'])} items")
    print(f"  Data points: {insights['data_points']}")

    return insights


def bq_list_datasets(
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Lists all datasets in a BigQuery project (Mock version).

    Args:
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        List[Dict[str, Any]]: List of dataset information dictionaries.
    """
    project = project_id or MOCK_PROJECT_ID
    print(f"[MOCK] bq_list_datasets called with project_id: {project}")
    
    mock_datasets = [
        {
            "dataset_id": MOCK_DATASET_ID,
            "project_id": project,
            "location": "US",
            "created": "2024-01-01T00:00:00Z",
            "modified": "2024-01-01T00:00:00Z",
        },
        {
            "dataset_id": "mock_dataset_2",
            "project_id": project,
            "location": "US",
            "created": "2024-01-02T00:00:00Z",
            "modified": "2024-01-02T00:00:00Z",
        },
    ]
    
    print(f"[MOCK] bq_list_datasets returning {len(mock_datasets)} datasets")
    for dataset in mock_datasets:
        print(f"  - {dataset['dataset_id']}")
    
    return mock_datasets


def bq_list_tables(
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Lists all tables in a BigQuery dataset (Mock version).

    Args:
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        List[Dict[str, Any]]: List of table information dictionaries.
    """
    project = project_id or MOCK_PROJECT_ID
    print(f"[MOCK] bq_list_tables called with dataset_id: {dataset_id}, project_id: {project}")
    
    mock_tables = [
        {
            "table_id": MOCK_TABLE_ID,
            "dataset_id": dataset_id,
            "project_id": project,
            "type": "TABLE",
            "created": "2024-01-01T00:00:00Z",
            "modified": "2024-01-01T00:00:00Z",
        },
        {
            "table_id": "mock_table_2",
            "dataset_id": dataset_id,
            "project_id": project,
            "type": "TABLE",
            "created": "2024-01-02T00:00:00Z",
            "modified": "2024-01-02T00:00:00Z",
        },
    ]
    
    print(f"[MOCK] bq_list_tables returning {len(mock_tables)} tables")
    for table in mock_tables:
        print(f"  - {table['table_id']}")
    
    return mock_tables


def bq_get_dataset_info(
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets information about a BigQuery dataset (Mock version).

    Args:
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        Dict[str, Any]: Dataset information dictionary.
    """
    project = project_id or MOCK_PROJECT_ID
    print(f"[MOCK] bq_get_dataset_info called with dataset_id: {dataset_id}, project_id: {project}")
    
    mock_info = {
        "dataset_id": dataset_id,
        "project_id": project,
        "location": "US",
        "created": "2024-01-01T00:00:00Z",
        "modified": "2024-01-01T00:00:00Z",
        "description": f"Mock dataset: {dataset_id}",
        "labels": {"environment": "mock", "purpose": "testing"},
        "default_table_expiration_ms": None,
        "default_partition_expiration_ms": None,
    }
    
    print(f"[MOCK] bq_get_dataset_info returning info for dataset: {dataset_id}")
    print(f"  Location: {mock_info['location']}")
    print(f"  Created: {mock_info['created']}")
    
    return mock_info


def bq_get_table_info(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets information about a BigQuery table (Mock version).

    Args:
        table_id (str): The table ID.
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        Dict[str, Any]: Table information dictionary.
    """
    project = project_id or MOCK_PROJECT_ID
    full_table_name = f"{project}.{dataset_id}.{table_id}"
    print(f"[MOCK] bq_get_table_info called with table: {full_table_name}")
    
    mock_info = {
        "table_id": table_id,
        "dataset_id": dataset_id,
        "project_id": project,
        "full_table_id": full_table_name,
        "type": "TABLE",
        "created": "2024-01-01T00:00:00Z",
        "modified": "2024-01-01T00:00:00Z",
        "description": f"Mock table: {table_id}",
        "num_rows": 1000,
        "num_bytes": 1024000,
        "location": "US",
    }
    
    print(f"[MOCK] bq_get_table_info returning info for table: {full_table_name}")
    print(f"  Type: {mock_info['type']}")
    print(f"  Rows: {mock_info['num_rows']}")
    print(f"  Size: {mock_info['num_bytes']} bytes")
    
    return mock_info


def bq_get_table_schema(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Gets the schema of a BigQuery table (Mock version).

    Args:
        table_id (str): The table ID.
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        List[Dict[str, Any]]: List of field schema dictionaries.
    """
    project = project_id or MOCK_PROJECT_ID
    full_table_name = f"{project}.{dataset_id}.{table_id}"
    print(f"[MOCK] bq_get_table_schema called with table: {full_table_name}")
    
    mock_schema = [
        {
            "name": "id",
            "type": "INTEGER",
            "mode": "REQUIRED",
            "description": "Primary key identifier",
        },
        {
            "name": "name",
            "type": "STRING",
            "mode": "NULLABLE",
            "description": "Name field",
        },
        {
            "name": "value",
            "type": "FLOAT",
            "mode": "NULLABLE",
            "description": "Numeric value",
        },
        {
            "name": "created_at",
            "type": "TIMESTAMP",
            "mode": "NULLABLE",
            "description": "Creation timestamp",
        },
    ]
    
    print(f"[MOCK] bq_get_table_schema returning {len(mock_schema)} fields")
    for field in mock_schema:
        print(f"  - {field['name']}: {field['type']} ({field['mode']})")
    
    return mock_schema


def bq_get_table_data(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    max_results: int = 10,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Gets sample data from a BigQuery table (Mock version).

    Args:
        table_id (str): The table ID.
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        max_results (int): Maximum number of rows to return. Defaults to 10.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        List[Dict[str, Any]]: List of row dictionaries.
    """
    project = project_id or MOCK_PROJECT_ID
    full_table_name = f"{project}.{dataset_id}.{table_id}"
    print(f"[MOCK] bq_get_table_data called with table: {full_table_name}, max_results: {max_results}")
    
    mock_data = [
        {"id": 1, "name": "Item 1", "value": 10.5, "created_at": "2024-01-01T00:00:00Z"},
        {"id": 2, "name": "Item 2", "value": 20.3, "created_at": "2024-01-02T00:00:00Z"},
        {"id": 3, "name": "Item 3", "value": 30.7, "created_at": "2024-01-03T00:00:00Z"},
        {"id": 4, "name": "Item 4", "value": 40.2, "created_at": "2024-01-04T00:00:00Z"},
        {"id": 5, "name": "Item 5", "value": 50.9, "created_at": "2024-01-05T00:00:00Z"},
    ]
    
    result = mock_data[:max_results]
    print(f"[MOCK] bq_get_table_data returning {len(result)} rows")
    for i, row in enumerate(result, 1):
        print(f"  Row {i}: {row}")
    
    return result


def bq_get_table_metadata(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets metadata about a BigQuery table (Mock version).

    Args:
        table_id (str): The table ID.
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        Dict[str, Any]: Table metadata dictionary.
    """
    project = project_id or MOCK_PROJECT_ID
    full_table_name = f"{project}.{dataset_id}.{table_id}"
    print(f"[MOCK] bq_get_table_metadata called with table: {full_table_name}")
    
    mock_metadata = {
        "table_id": table_id,
        "dataset_id": dataset_id,
        "project_id": project,
        "full_table_id": full_table_name,
        "type": "TABLE",
        "created": "2024-01-01T00:00:00Z",
        "modified": "2024-01-01T00:00:00Z",
        "description": f"Mock table metadata for {table_id}",
        "labels": {"environment": "mock", "purpose": "testing"},
        "num_rows": 1000,
        "num_bytes": 1024000,
        "location": "US",
        "expiration_time": None,
        "partitioning": None,
        "clustering": None,
    }
    
    print(f"[MOCK] bq_get_table_metadata returning metadata for table: {full_table_name}")
    print(f"  Description: {mock_metadata['description']}")
    print(f"  Labels: {mock_metadata['labels']}")
    print(f"  Expiration: {mock_metadata['expiration_time']}")
    
    return mock_metadata


def bq_get_table_statistics(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """Gets statistics about a BigQuery table (Mock version).

    Args:
        table_id (str): The table ID.
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        Dict[str, Any]: Table statistics dictionary.
    """
    project = project_id or MOCK_PROJECT_ID
    full_table_name = f"{project}.{dataset_id}.{table_id}"
    print(f"[MOCK] bq_get_table_statistics called with table: {full_table_name}")
    
    mock_stats = {
        "table_id": table_id,
        "dataset_id": dataset_id,
        "project_id": project,
        "num_rows": 1000,
        "num_bytes": 1024000,
        "num_long_term_bytes": 1024000,
        "num_total_logical_bytes": 2048000,
        "num_active_logical_bytes": 1024000,
        "num_long_term_logical_bytes": 1024000,
        "last_modified_time": "2024-01-01T00:00:00Z",
        "column_statistics": {
            "id": {"min": 1, "max": 1000, "null_count": 0},
            "name": {"distinct_count": 950, "null_count": 0},
            "value": {"min": 0.0, "max": 100.0, "avg": 50.0, "null_count": 5},
            "created_at": {"min": "2024-01-01T00:00:00Z", "max": "2024-12-31T23:59:59Z", "null_count": 0},
        },
    }
    
    print(f"[MOCK] bq_get_table_statistics returning statistics for table: {full_table_name}")
    print(f"  Total rows: {mock_stats['num_rows']}")
    print(f"  Total bytes: {mock_stats['num_bytes']}")
    print(f"  Last modified: {mock_stats['last_modified_time']}")
    print(f"  Column statistics: {len(mock_stats['column_statistics'])} columns")
    
    return mock_stats


def bq_get_table_partitions(
    table_id: str,
    dataset_id: str,
    project_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> List[Dict[str, Any]]:
    """Gets partition information for a BigQuery table (Mock version).

    Args:
        table_id (str): The table ID.
        dataset_id (str): The dataset ID.
        project_id (str, optional): The project ID. Defaults to mock project.
        tool_context (ToolContext, optional): The tool context.

    Returns:
        List[Dict[str, Any]]: List of partition information dictionaries.
    """
    project = project_id or MOCK_PROJECT_ID
    full_table_name = f"{project}.{dataset_id}.{table_id}"
    print(f"[MOCK] bq_get_table_partitions called with table: {full_table_name}")
    
    # Mock partitioned table with date partitions
    mock_partitions = [
        {
            "partition_id": "20240101",
            "creation_time": "2024-01-01T00:00:00Z",
            "last_modified_time": "2024-01-01T00:00:00Z",
            "num_rows": 100,
            "num_bytes": 102400,
        },
        {
            "partition_id": "20240102",
            "creation_time": "2024-01-02T00:00:00Z",
            "last_modified_time": "2024-01-02T00:00:00Z",
            "num_rows": 150,
            "num_bytes": 153600,
        },
        {
            "partition_id": "20240103",
            "creation_time": "2024-01-03T00:00:00Z",
            "last_modified_time": "2024-01-03T00:00:00Z",
            "num_rows": 200,
            "num_bytes": 204800,
        },
    ]
    
    print(f"[MOCK] bq_get_table_partitions returning {len(mock_partitions)} partitions")
    for partition in mock_partitions:
        print(f"  Partition {partition['partition_id']}: {partition['num_rows']} rows, {partition['num_bytes']} bytes")
    
    return mock_partitions
