from amsdal_utils.query.data_models.order_by import OrderBy as OrderBy
from typing import Any

def get_nested_value(item: dict[str, Any], field_name: str) -> Any:
    """
    Retrieves a nested value from a dictionary based on a field name.

    Args:
        item (dict[str, Any]): The dictionary to retrieve the value from.
        field_name (str): The field name, with nested fields separated by double underscores.

    Returns:
        Any: The value of the nested field, or None if any field in the path does not exist.
    """
def sort_items(items: list[dict[str, Any]], order_by_list: list[OrderBy] | None) -> list[dict[str, Any]]:
    """
    Sorts a list of dictionaries based on a list of OrderBy objects.

    Args:
        items (list[dict[str, Any]]): The list of dictionaries to sort.
        order_by_list (list[OrderBy] | None): The list of OrderBy objects specifying the sort order.

    Returns:
        list[dict[str, Any]]: The sorted list of dictionaries.
    """
