import json
import logging
from typing import Callable, Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def apply_rules(
        rules: Dict[str, Dict[str, Any]],
        request: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Applies transformation rules to the request data.

    Args:
        rules (Dict[str, Dict[str, Any]]): Dictionary containing rules to be applied.
        request (Dict[str, Any]): Input request data.

    Returns:
        Optional[Dict[str, Any]]: Resulting dictionary after applying the rules.
    """
    try:
        def get_value_from_keys(keys: List[str], request_data: Dict[str, Any]) -> Optional[Any]:
            """Helper function to extract value from the request using dot-separated keys."""
            for key in keys:
                parts = key.split('.')
                value = request_data
                for part in parts:
                    if isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        value = None
                        break
                if value is not None:
                    return value
            return None

        result: Dict[str, Any] = {}
        is_valid = True

        for rule_key, rule_props in rules.items():
            keys = rule_props.get('keys', [])
            default_value = rule_props.get('default_value')
            handler_function: Optional[Callable[[Any, Dict[str, Any]], Any]] = rule_props.get('handler_function')
            mandatory = rule_props.get('mandatory', False)
            skip_if_missing = rule_props.get('skip_if_missing', False)

            # Skip processing if keys are missing and skip_if_missing is True
            if skip_if_missing and not keys:
                continue

            # Get value from request or use default value
            if not keys:
                value = default_value
            else:
                value = get_value_from_keys(keys, request)
                if value is None:
                    if mandatory:
                        is_valid = False
                    if skip_if_missing:
                        continue
                    value = default_value

            # Apply handler function if present
            if handler_function:
                value = handler_function(value, data=request)

            # Populate the result dictionary using dot notation
            parts = rule_key.split('.')
            current_level = result
            for part in parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            current_level[parts[-1]] = value

        # Handle special case for anonymous user
        raw_data = result.get("RawData", {}).get("UserInfo", {})
        if raw_data.get("AuthorName") == "Anonymous":
            raw_data["AuthorSocialID"] = "0"
        result["RawData"] = json.dumps(result.get("RawData", {}))

        return result

    except Exception as ex:
        logger.error(f"Error in apply_rules: {ex}")
        return None
