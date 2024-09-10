from typing import List, Dict, Any, Optional


def extract_required_fields(settings: List[Dict[str, Any]], required_fields: List[str]) -> List[Dict[str, Any]]:
    """Extract only the required fields from the settings."""
    extracted_settings = []

    for setting in settings:
        extracted = {field: setting.get(field) for field in required_fields}
        extracted_settings.append(extracted)

    return extracted_settings


def build_single_key_lookup_table(
        settings: List[Dict[str, Any]],
        key_field: str
) -> Dict[Any, List[Dict[str, Any]]]:
    """Build a lookup table with a single key field."""

    lookup_table = {}

    for setting in settings:
        key_value = setting.get(key_field)

        if key_value is not None:
            if key_value in lookup_table:
                lookup_table[key_value].append(setting)
            else:
                lookup_table[key_value] = [setting]

    return lookup_table


def get_setting_by_single_key(
        lookup_table: Dict[Any, List[Dict[str, Any]]],
        key_value: Any
) -> Optional[List[Dict[str, Any]]]:
    """Fetch settings based on a single key in O(1) time."""
    return lookup_table.get(key_value, None)
