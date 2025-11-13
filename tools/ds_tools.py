'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-13
Description: Tools for DS (Data Storage) agent - Mock implementations
'''
from typing import Any, Dict, List, Optional, Union
import json
from datetime import datetime
from ..config import config


def insert_into_bigquery(
    dataset_id: str,
    table_id: str,
    data: List[Dict[str, Any]],
    write_disposition: str = "WRITE_APPEND"
) -> Dict[str, Any]:
    """Insert data into BigQuery table.
    
    Args:
        dataset_id (str): BigQuery dataset ID.
        table_id (str): BigQuery table ID.
        data (List[Dict[str, Any]]): Data rows to insert.
        write_disposition (str): Write disposition mode (WRITE_APPEND, WRITE_TRUNCATE, WRITE_EMPTY).
    
    Returns:
        Dict[str, Any]: Insert operation results.
    """
    return {
        "status": "success",
        "tool": "insert_into_bigquery",
        "project_id": config.project_id,
        "dataset_id": dataset_id,
        "table_id": table_id,
        "write_disposition": write_disposition,
        "result": {
            "rows_inserted": len(data),
            "job_id": "mock_bq_job_12345",
            "table": f"{config.project_id}.{dataset_id}.{table_id}",
            "inserted_at": "2025-11-13T10:00:00Z"
        },
        "message": f"Successfully inserted {len(data)} rows into BigQuery (mock)"
    }


def insert_into_gcs(
    bucket_name: str,
    file_path: str,
    data: Union[List[Dict[str, Any]], str, bytes],
    file_format: str = "json",
    content_type: Optional[str] = None
) -> Dict[str, Any]:
    """Insert data into Google Cloud Storage (GCS).
    
    Args:
        bucket_name (str): GCS bucket name.
        file_path (str): Path within the bucket to store the file.
        data (Union[List[Dict], str, bytes]): Data to store (list of dicts, JSON string, or bytes).
        file_format (str): File format - 'json', 'csv', 'parquet', 'text'. Defaults to 'json'.
        content_type (Optional[str]): MIME content type. If None, inferred from file_format.
    
    Returns:
        Dict[str, Any]: Insert operation results.
    """
    # Determine content type
    if content_type is None:
        content_type_map = {
            "json": "application/json",
            "csv": "text/csv",
            "parquet": "application/octet-stream",
            "text": "text/plain"
        }
        content_type = content_type_map.get(file_format, "application/octet-stream")
    
    # Calculate data size (mock)
    if isinstance(data, list):
        data_size = len(json.dumps(data))
    elif isinstance(data, str):
        data_size = len(data.encode('utf-8'))
    elif isinstance(data, bytes):
        data_size = len(data)
    else:
        data_size = len(str(data))
    
    return {
        "status": "success",
        "tool": "insert_into_gcs",
        "bucket_name": bucket_name,
        "file_path": file_path,
        "file_format": file_format,
        "content_type": content_type,
        "result": {
            "uploaded": True,
            "file_size": data_size,
            "gcs_uri": f"gs://{bucket_name}/{file_path}",
            "uploaded_at": datetime.now().isoformat(),
            "records_count": len(data) if isinstance(data, list) else 1
        },
        "message": f"Successfully uploaded data to GCS: gs://{bucket_name}/{file_path} (mock)"
    }


def insert_into_nosql(
    database_name: str,
    collection_name: str,
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    database_type: str = "firestore"
) -> Dict[str, Any]:
    """Insert data into NoSQL database (Firestore, MongoDB, etc.).
    
    Args:
        database_name (str): Database name.
        collection_name (str): Collection/table name.
        data (Union[List[Dict], Dict]): Data to insert (single document or list of documents).
        database_type (str): Type of NoSQL database - 'firestore', 'mongodb', etc. Defaults to 'firestore'.
    
    Returns:
        Dict[str, Any]: Insert operation results.
    """
    # Normalize data to list
    if isinstance(data, dict):
        data = [data]
    
    inserted_count = len(data)
    
    return {
        "status": "success",
        "tool": "insert_into_nosql",
        "database_type": database_type,
        "database_name": database_name,
        "collection_name": collection_name,
        "result": {
            "inserted": True,
            "documents_inserted": inserted_count,
            "database": database_name,
            "collection": collection_name,
            "inserted_at": datetime.now().isoformat(),
            "document_ids": [f"doc_{i+1}" for i in range(inserted_count)]  # Mock document IDs
        },
        "message": f"Successfully inserted {inserted_count} documents into {database_type} (mock)"
    }


def insert_into_sql(
    connection_string: str,
    table_name: str,
    data: List[Dict[str, Any]],
    database_type: str = "postgresql",
    schema: Optional[str] = None
) -> Dict[str, Any]:
    """Insert data into SQL database (PostgreSQL, MySQL, SQL Server, etc.).
    
    Args:
        connection_string (str): Database connection string or connection identifier.
        table_name (str): Target table name.
        data (List[Dict[str, Any]]): Data rows to insert.
        database_type (str): Type of SQL database - 'postgresql', 'mysql', 'sqlserver', etc. Defaults to 'postgresql'.
        schema (Optional[str]): Database schema name. If None, uses default schema.
    
    Returns:
        Dict[str, Any]: Insert operation results.
    """
    inserted_count = len(data)
    full_table_name = f"{schema}.{table_name}" if schema else table_name
    
    return {
        "status": "success",
        "tool": "insert_into_sql",
        "database_type": database_type,
        "connection_string": connection_string[:20] + "..." if len(connection_string) > 20 else connection_string,  # Mask sensitive info
        "table_name": full_table_name,
        "result": {
            "inserted": True,
            "rows_inserted": inserted_count,
            "database_type": database_type,
            "table": full_table_name,
            "inserted_at": datetime.now().isoformat(),
            "transaction_id": f"txn_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        },
        "message": f"Successfully inserted {inserted_count} rows into {database_type} table {full_table_name} (mock)"
    }


def logging_sth(
    log_level: str,
    message: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Log something with specified level and message.
    
    Args:
        log_level (str): Log level (INFO, WARNING, ERROR, DEBUG).
        message (str): Log message.
        metadata (Optional[Dict[str, Any]]): Optional metadata to include in log.
    
    Returns:
        Dict[str, Any]: Logging result.
    """
    return {
        "status": "success",
        "tool": "logging_sth",
        "log_level": log_level,
        "message": message,
        "metadata": metadata or {},
        "result": {
            "logged": True,
            "log_id": "log_12345",
            "timestamp": "2025-11-13T10:00:00Z",
            "log_entry": {
                "level": log_level,
                "message": message,
                "metadata": metadata or {}
            }
        },
        "message": f"Log entry created with level {log_level} (mock)"
    }


def trigger_sth(
    trigger_name: str,
    parameters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Trigger something (workflow, process, etc.).
    
    Args:
        trigger_name (str): Name of the trigger/workflow/process to trigger.
        parameters (Optional[Dict[str, Any]]): Optional parameters for the trigger.
    
    Returns:
        Dict[str, Any]: Trigger execution result.
    """
    return {
        "status": "success",
        "tool": "trigger_sth",
        "trigger_name": trigger_name,
        "parameters": parameters or {},
        "result": {
            "triggered": True,
            "execution_id": "exec_12345",
            "trigger_name": trigger_name,
            "status": "started",
            "triggered_at": "2025-11-13T10:00:00Z",
            "parameters": parameters or {}
        },
        "message": f"Trigger '{trigger_name}' executed successfully (mock)"
    }

