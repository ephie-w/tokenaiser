'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-13
Description: Tools for Ingestion agent - Mock implementations
'''
from typing import Any, Dict, List, Optional
import json


def fetch_apigee(api_endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch data from Apigee API.
    
    Args:
        api_endpoint (str): The API endpoint to fetch from.
        params (Optional[Dict[str, Any]]): Optional query parameters.
    
    Returns:
        Dict[str, Any]: Mock API response data.
    """
    return {
        "status": "success",
        "source": "apigee",
        "endpoint": api_endpoint,
        "params": params or {},
        "data": {
            "message": "This is a mock response from Apigee API",
            "timestamp": "2025-11-13T10:00:00Z",
            "records": [
                {"id": 1, "name": "record1", "value": "data1"},
                {"id": 2, "name": "record2", "value": "data2"},
            ]
        }
    }


def query_bq(query: str, dataset_id: Optional[str] = None, table_id: Optional[str] = None) -> Dict[str, Any]:
    """Query BigQuery table.
    
    Args:
        query (str): SQL query string or table identifier.
        dataset_id (Optional[str]): Dataset ID if querying a specific table.
        table_id (Optional[str]): Table ID if querying a specific table.
    
    Returns:
        Dict[str, Any]: Mock query results.
    """
    return {
        "status": "success",
        "source": "bigquery",
        "query": query,
        "dataset_id": dataset_id,
        "table_id": table_id,
        "results": [
            {"column1": "value1", "column2": "value2", "column3": 123},
            {"column1": "value3", "column2": "value4", "column3": 456},
        ],
        "row_count": 2,
        "message": "This is a mock BigQuery query result"
    }


def fetch_pub(topic: str, subscription: Optional[str] = None, max_messages: int = 10) -> Dict[str, Any]:
    """Fetch messages from Pub/Sub.
    
    Args:
        topic (str): Pub/Sub topic name.
        subscription (Optional[str]): Subscription name.
        max_messages (int): Maximum number of messages to fetch.
    
    Returns:
        Dict[str, Any]: Mock Pub/Sub messages.
    """
    return {
        "status": "success",
        "source": "pubsub",
        "topic": topic,
        "subscription": subscription,
        "max_messages": max_messages,
        "messages": [
            {
                "message_id": "msg_001",
                "data": "Message 1 data",
                "attributes": {"key1": "value1"},
                "publish_time": "2025-11-13T10:00:00Z"
            },
            {
                "message_id": "msg_002",
                "data": "Message 2 data",
                "attributes": {"key2": "value2"},
                "publish_time": "2025-11-13T10:01:00Z"
            }
        ],
        "message_count": 2
    }


def fetch_Snowflake(query: str, warehouse: Optional[str] = None, database: Optional[str] = None) -> Dict[str, Any]:
    """Fetch data from Snowflake.
    
    Args:
        query (str): SQL query to execute.
        warehouse (Optional[str]): Snowflake warehouse name.
        database (Optional[str]): Snowflake database name.
    
    Returns:
        Dict[str, Any]: Mock Snowflake query results.
    """
    return {
        "status": "success",
        "source": "snowflake",
        "query": query,
        "warehouse": warehouse,
        "database": database,
        "results": [
            {"id": 1, "name": "snowflake_record1", "value": 100},
            {"id": 2, "name": "snowflake_record2", "value": 200},
        ],
        "row_count": 2,
        "message": "This is a mock Snowflake query result"
    }


# Alias for typo in YAML (fethc_apigee -> fetch_apigee)
fethc_apigee = fetch_apigee


def fetch_crm(record_type: str, record_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch data from CRM system.
    
    Args:
        record_type (str): Type of CRM record (e.g., 'contact', 'account', 'opportunity').
        record_id (Optional[str]): Specific record ID to fetch.
        filters (Optional[Dict[str, Any]]): Optional filters for querying records.
    
    Returns:
        Dict[str, Any]: Mock CRM data.
    """
    return {
        "status": "success",
        "source": "crm",
        "record_type": record_type,
        "record_id": record_id,
        "filters": filters or {},
        "records": [
            {
                "id": "crm_001",
                "type": record_type,
                "name": f"CRM {record_type} 1",
                "status": "active",
                "created_date": "2025-11-13T10:00:00Z"
            },
            {
                "id": "crm_002",
                "type": record_type,
                "name": f"CRM {record_type} 2",
                "status": "active",
                "created_date": "2025-11-13T10:01:00Z"
            }
        ],
        "record_count": 2,
        "message": "This is a mock CRM fetch result"
    }


def fetch_gcs(bucket_name: str, file_path: str) -> Dict[str, Any]:
    """Fetch data from GCS.
    
    Args:
        bucket_name (str): GCS bucket name.
        file_path (str): GCS file path.
    
    Returns:
        Dict[str, Any]: Mock GCS data.
    """
    return {
        "status": "success",
        "source": "gcs",
        "bucket_name": bucket_name,
        "file_path": file_path,
        "data": {
            "message": "This is a mock GCS data",
            "timestamp": "2025-11-13T10:00:00Z",
            "records": [
                {"id": 1, "name": "record1", "value": "data1"},
                {"id": 2, "name": "record2", "value": "data2"},
            ]
        }
    }