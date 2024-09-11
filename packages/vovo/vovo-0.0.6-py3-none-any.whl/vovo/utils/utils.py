from typing import Any, Set


def get_pydantic_field_names(pydantic_cls: Any) -> Set[str]:
    """Get field names, including aliases, for a pydantic class.

       Args:
           pydantic_cls: Pydantic class.

       Returns:
           Set[str]: Field names.
    """
    all_required_field_names = set()
    for name, field in pydantic_cls.model_fields.items():
        all_required_field_names.add(name)
        if field.alias:
            all_required_field_names.add(field.alias)

    return all_required_field_names
