'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-13 13:46:08
LastEditors: ephie && ephiewangyf@gmail.com
LastEditTime: 2025-11-13 14:19:54
FilePath: /sample/tokenaiser/tools/crm.py
Description: CRM tools - Note: fetch_crm is now in ingestion_tools.py
'''
from typing import Any, Dict, Optional

# This file is kept for backward compatibility
# The actual fetch_crm implementation is in ingestion_tools.py
def fetch_crm(record_type: str = "contact", record_id: Optional[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Fetch data from CRM system.
    
    Args:
        record_type (str): Type of CRM record (e.g., 'contact', 'account', 'opportunity').
        record_id (Optional[str]): Specific record ID to fetch.
        filters (Optional[Dict[str, Any]]): Optional filters for querying records.
    
    Returns:
        Dict[str, Any]: Mock CRM data.
    """
    from .ingestion_tools import fetch_crm as _fetch_crm
    return _fetch_crm(record_type, record_id, filters)