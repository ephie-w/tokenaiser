"""Mock tools for dispatcher agent."""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def dispatch_consumer(message: str = "") -> Dict[str, Any]:
    """Invoke API to dispatch notification to consumer channel (Mock version).
    
    Args:
        message: Optional message to include in the dispatch.
    
    Returns:
        dict: Status and dispatch event information.
    """
    logger.debug("dispatch_consumer (mock) - message: %s", message)
    
    # Mock dispatch logic
    mock_response = {
        "status": "success",
        "dispatch_event": "Subscriptions have dipped by 10% against daily average",
        "channel": "consumer",
        "message": message if message else "Default consumer notification",
        "timestamp": "2024-01-01T00:00:00Z",
    }
    
    logger.debug("dispatch_consumer (mock) - response: %s", mock_response)
    return mock_response


def dispatch_editorial(message: str = "") -> Dict[str, Any]:
    """Invoke API to dispatch notification to editorial channel (Mock version).
    
    Args:
        message: Optional message to include in the dispatch.
    
    Returns:
        dict: Status and dispatch event information.
    """
    logger.debug("dispatch_editorial (mock) - message: %s", message)
    
    # Mock dispatch logic
    mock_response = {
        "status": "success",
        "dispatch_event": "Conversion rate has decreased by 20%",
        "channel": "editorial",
        "message": message if message else "Default editorial notification",
        "timestamp": "2024-01-01T00:00:00Z",
    }
    
    logger.debug("dispatch_editorial (mock) - response: %s", mock_response)
    return mock_response


def apihub(
    endpoint: str = "",
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    action: str = "fetch",
) -> Dict[str, Any]:
    """API Hub for external data retrieval, API calls, and data fetching (Mock version).
    
    This tool handles:
    - External data retrieval
    - API calls
    - Schema lookup
    - Metadata retrieval
    - Automated data access
    - Interactions with external systems
    
    Args:
        endpoint: API endpoint URL or resource identifier.
        method: HTTP method (GET, POST, PUT, DELETE). Defaults to "GET".
        params: Query parameters for the API call.
        data: Request body data for POST/PUT requests.
        action: Type of action to perform (fetch, schema, metadata, etc.). Defaults to "fetch".
    
    Returns:
        dict: Response containing status, data, and metadata.
    """
    logger.debug("apihub (mock) - endpoint: %s, method: %s, action: %s, params: %s", 
                 endpoint, method, action, params)
    
    # Mock API hub logic based on action type
    if action == "schema" or "schema" in endpoint.lower():
        mock_response = {
            "status": "success",
            "action": "schema_lookup",
            "endpoint": endpoint or "mock_api/schema",
            "data": {
                "tables": [
                    {
                        "name": "users",
                        "columns": ["id", "name", "email", "created_at"],
                        "type": "table"
                    },
                    {
                        "name": "orders",
                        "columns": ["id", "user_id", "amount", "status", "created_at"],
                        "type": "table"
                    }
                ],
                "schemas": {
                    "users": {
                        "id": "INTEGER",
                        "name": "STRING",
                        "email": "STRING",
                        "created_at": "TIMESTAMP"
                    },
                    "orders": {
                        "id": "INTEGER",
                        "user_id": "INTEGER",
                        "amount": "FLOAT",
                        "status": "STRING",
                        "created_at": "TIMESTAMP"
                    }
                }
            },
            "metadata": {
                "source": "mock_api",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }
    elif action == "metadata" or "metadata" in endpoint.lower():
        mock_response = {
            "status": "success",
            "action": "metadata_retrieval",
            "endpoint": endpoint or "mock_api/metadata",
            "data": {
                "version": "1.0.0",
                "last_updated": "2024-01-01T00:00:00Z",
                "total_tables": 2,
                "total_records": 1000,
                "database_name": "mock_database",
                "location": "US"
            },
            "metadata": {
                "source": "mock_api",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }
    else:
        # Default fetch action
        mock_response = {
            "status": "success",
            "action": "data_fetch",
            "endpoint": endpoint or "mock_api/data",
            "method": method,
            "data": [
                {"id": 1, "name": "Item 1", "value": 100, "status": "active"},
                {"id": 2, "name": "Item 2", "value": 200, "status": "active"},
                {"id": 3, "name": "Item 3", "value": 150, "status": "inactive"},
            ],
            "pagination": {
                "page": 1,
                "per_page": 10,
                "total": 3,
                "total_pages": 1
            },
            "metadata": {
                "source": "mock_api",
                "timestamp": "2024-01-01T00:00:00Z",
                "params": params or {},
                "request_data": data or {}
            }
        }
    
    logger.debug("apihub (mock) - response: %s", mock_response)
    return mock_response

