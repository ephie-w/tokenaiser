'''
Author: Yifei Wang
Github: ephiewangyf@gmail.com
Date: 2025-11-13
Description: Tools for Integration agent - Mock implementations
'''
from typing import Any, Dict, List, Optional, Union
import json
from datetime import datetime


def mock_boomi(source_data: Any, target_system: str, mapping_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Mock Boomi integration tool for data transformation and integration.
    
    Args:
        source_data (Any): Source data to integrate (can be dict, list, or string).
        target_system (str): Target system identifier.
        mapping_config (Optional[Dict[str, Any]]): Optional field mapping configuration.
    
    Returns:
        Dict[str, Any]: Integration results.
    """
    return {
        "status": "success",
        "tool": "mock_boomi",
        "source_data_type": type(source_data).__name__,
        "target_system": target_system,
        "mapping_config": mapping_config or {},
        "result": {
            "integrated": True,
            "records_processed": 10,
            "records_successful": 10,
            "records_failed": 0,
            "transformation_applied": True,
            "target_system_response": {
                "status": "accepted",
                "batch_id": "batch_12345",
                "processed_at": "2025-11-13T10:00:00Z"
            }
        },
        "message": "Data integrated successfully using mock Boomi (mock)"
    }


def merge_csv(
    csv_data_list: List[Union[str, List[Dict[str, Any]]]],
    merge_key: Optional[str] = None,
    merge_strategy: str = "union"
) -> Dict[str, Any]:
    """Merge multiple CSV data sources into a single dataset.
    
    Args:
        csv_data_list (List[Union[str, List[Dict]]]): List of CSV data (as strings or parsed lists).
        merge_key (Optional[str]): Key to use for merging (if inner/outer join strategy).
        merge_strategy (str): Merge strategy - 'union', 'inner', 'outer'. Defaults to 'union'.
    
    Returns:
        Dict[str, Any]: Merged CSV data and statistics.
    """
    # Mock: Parse and merge CSV data
    total_records = sum(len(data) if isinstance(data, list) else 10 for data in csv_data_list)
    
    return {
        "status": "success",
        "tool": "merge_csv",
        "merge_strategy": merge_strategy,
        "merge_key": merge_key,
        "result": {
            "merged": True,
            "input_sources": len(csv_data_list),
            "total_records": total_records,
            "merged_records": total_records,
            "sample_data": [
                {"id": 1, "name": "merged_record1", "value": 100},
                {"id": 2, "name": "merged_record2", "value": 200},
            ]
        },
        "message": f"Successfully merged {len(csv_data_list)} CSV sources (mock)"
    }


def normalize_json(
    json_data: Union[str, Dict, List],
    schema: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Normalize JSON data into a consistent structure.
    
    Args:
        json_data (Union[str, Dict, List]): JSON data to normalize (string, dict, or list).
        schema (Optional[Dict[str, Any]]): Optional target schema for normalization.
    
    Returns:
        Dict[str, Any]: Normalized JSON data and metadata.
    """
    # Mock: Normalize JSON structure
    if isinstance(json_data, str):
        try:
            parsed = json.loads(json_data)
        except:
            parsed = {"raw": json_data}
    else:
        parsed = json_data
    
    return {
        "status": "success",
        "tool": "normalize_json",
        "input_type": type(json_data).__name__,
        "result": {
            "normalized": True,
            "structure": "tabular" if isinstance(parsed, list) else "object",
            "record_count": len(parsed) if isinstance(parsed, list) else 1,
            "normalized_data": parsed if isinstance(parsed, list) else [parsed],
            "schema_applied": schema is not None
        },
        "message": "JSON data normalized successfully (mock)"
    }


def clean_dates(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    date_fields: Optional[List[str]] = None,
    target_format: str = "ISO8601"
) -> Dict[str, Any]:
    """Clean and standardize date/time formats in data.
    
    Args:
        data (Union[List[Dict], Dict]): Data containing date fields.
        date_fields (Optional[List[str]]): List of field names containing dates. If None, auto-detect.
        target_format (str): Target date format. Defaults to 'ISO8601'.
    
    Returns:
        Dict[str, Any]: Cleaned data with standardized dates.
    """
    # Mock: Clean date formats
    if isinstance(data, dict):
        data = [data]
    
    cleaned_count = 0
    if date_fields:
        cleaned_count = len(date_fields) * len(data)
    else:
        # Auto-detect date fields
        cleaned_count = len(data) * 2  # Mock: assume 2 date fields per record
    
    return {
        "status": "success",
        "tool": "clean_dates",
        "target_format": target_format,
        "date_fields": date_fields or ["auto-detected"],
        "result": {
            "cleaned": True,
            "records_processed": len(data),
            "dates_cleaned": cleaned_count,
            "target_format": target_format,
            "sample_cleaned": [
                {
                    "id": 1,
                    "date_field": "2025-11-13T10:00:00Z",
                    "created_at": "2025-11-13T10:00:00Z"
                }
            ]
        },
        "message": f"Cleaned {cleaned_count} date fields to {target_format} format (mock)"
    }


def deduplicate(
    data: List[Dict[str, Any]],
    key_fields: Optional[List[str]] = None,
    strategy: str = "keep_first"
) -> Dict[str, Any]:
    """Remove duplicate records from data.
    
    Args:
        data (List[Dict[str, Any]]): List of records to deduplicate.
        key_fields (Optional[List[str]]): Fields to use for duplicate detection. If None, use all fields.
        strategy (str): Deduplication strategy - 'keep_first', 'keep_last', 'keep_none'. Defaults to 'keep_first'.
    
    Returns:
        Dict[str, Any]: Deduplicated data and statistics.
    """
    # Mock: Deduplicate records
    original_count = len(data)
    duplicate_count = max(0, original_count - int(original_count * 0.9))  # Mock: 10% duplicates
    deduplicated_count = original_count - duplicate_count
    
    return {
        "status": "success",
        "tool": "deduplicate",
        "strategy": strategy,
        "key_fields": key_fields or ["all_fields"],
        "result": {
            "deduplicated": True,
            "original_count": original_count,
            "duplicate_count": duplicate_count,
            "deduplicated_count": deduplicated_count,
            "deduplicated_data": data[:deduplicated_count] if deduplicated_count <= len(data) else data
        },
        "message": f"Removed {duplicate_count} duplicate records (mock)"
    }


def map_schema(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    field_mapping: Dict[str, str],
    default_value: Any = None
) -> Dict[str, Any]:
    """Map data fields to a new schema using field mapping.
    
    Args:
        data (Union[List[Dict], Dict]): Data to map.
        field_mapping (Dict[str, str]): Mapping from old field names to new field names.
        default_value (Any): Default value for fields not in mapping. Defaults to None.
    
    Returns:
        Dict[str, Any]: Mapped data with new schema.
    """
    # Mock: Map schema
    if isinstance(data, dict):
        data = [data]
    
    mapped_count = len(data)
    
    return {
        "status": "success",
        "tool": "map_schema",
        "field_mapping": field_mapping,
        "result": {
            "mapped": True,
            "records_processed": mapped_count,
            "fields_mapped": len(field_mapping),
            "mapped_data": [
                {field_mapping.get(k, k): v for k, v in record.items()}
                for record in data[:min(3, len(data))]  # Sample
            ]
        },
        "message": f"Mapped {len(field_mapping)} fields for {mapped_count} records (mock)"
    }


def filter_fields(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    fields_to_keep: Optional[List[str]] = None,
    fields_to_remove: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Filter fields from data - keep or remove specified fields.
    
    Args:
        data (Union[List[Dict], Dict]): Data to filter.
        fields_to_keep (Optional[List[str]]): List of fields to keep. If provided, only these fields are kept.
        fields_to_remove (Optional[List[str]]): List of fields to remove. Ignored if fields_to_keep is provided.
    
    Returns:
        Dict[str, Any]: Filtered data with selected fields.
    """
    # Mock: Filter fields
    if isinstance(data, dict):
        data = [data]
    
    if fields_to_keep:
        filtered_data = [
            {k: v for k, v in record.items() if k in fields_to_keep}
            for record in data
        ]
        action = f"kept {len(fields_to_keep)} fields"
    elif fields_to_remove:
        filtered_data = [
            {k: v for k, v in record.items() if k not in fields_to_remove}
            for record in data
        ]
        action = f"removed {len(fields_to_remove)} fields"
    else:
        filtered_data = data
        action = "no filtering applied"
    
    return {
        "status": "success",
        "tool": "filter_fields",
        "fields_to_keep": fields_to_keep,
        "fields_to_remove": fields_to_remove,
        "result": {
            "filtered": True,
            "records_processed": len(data),
            "action": action,
            "filtered_data": filtered_data[:min(3, len(filtered_data))]  # Sample
        },
        "message": f"Field filtering completed: {action} (mock)"
    }


def transform_numeric(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    numeric_fields: Optional[List[str]] = None,
    transformations: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Transform numeric fields in data (rounding, scaling, etc.).
    
    Args:
        data (Union[List[Dict], Dict]): Data containing numeric fields.
        numeric_fields (Optional[List[str]]): List of numeric field names. If None, auto-detect.
        transformations (Optional[Dict[str, str]]): Transformations to apply, e.g., {'field': 'round:2', 'field2': 'scale:100'}.
    
    Returns:
        Dict[str, Any]: Transformed data with modified numeric fields.
    """
    # Mock: Transform numeric fields
    if isinstance(data, dict):
        data = [data]
    
    if numeric_fields is None:
        numeric_fields = ["value", "amount", "price", "quantity"]  # Mock auto-detection
    
    transformed_count = len(numeric_fields) * len(data)
    
    return {
        "status": "success",
        "tool": "transform_numeric",
        "numeric_fields": numeric_fields,
        "transformations": transformations or {},
        "result": {
            "transformed": True,
            "records_processed": len(data),
            "fields_transformed": len(numeric_fields),
            "transformations_applied": transformed_count,
            "transformed_data": data[:min(3, len(data))]  # Sample
        },
        "message": f"Transformed {transformed_count} numeric values (mock)"
    }


def validate_data(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    validation_rules: Optional[Dict[str, Any]] = None,
    strict: bool = False
) -> Dict[str, Any]:
    """Validate data against specified rules.
    
    Args:
        data (Union[List[Dict], Dict]): Data to validate.
        validation_rules (Optional[Dict[str, Any]]): Validation rules, e.g., {'field': {'type': 'string', 'required': True}}.
        strict (bool): If True, fail on first validation error. Defaults to False.
    
    Returns:
        Dict[str, Any]: Validation results with pass/fail status and error details.
    """
    # Mock: Validate data
    if isinstance(data, dict):
        data = [data]
    
    validation_passed = True
    errors = []
    
    if validation_rules:
        # Mock validation checks
        for rule_field, rule_config in validation_rules.items():
            for record in data:
                if rule_config.get("required") and rule_field not in record:
                    validation_passed = False
                    errors.append(f"Missing required field: {rule_field}")
                    if strict:
                        break
            if strict and not validation_passed:
                break
    
    return {
        "status": "success" if validation_passed else "validation_failed",
        "tool": "validate_data",
        "validation_rules": validation_rules or {},
        "strict_mode": strict,
        "result": {
            "validated": True,
            "validation_passed": validation_passed,
            "records_checked": len(data),
            "errors": errors,
            "error_count": len(errors)
        },
        "message": f"Validation {'passed' if validation_passed else 'failed'} with {len(errors)} errors (mock)"
    }

