from django.db.models import Q
from typing import Any, Dict, Optional

def apply_filters_and_search(queryset, filters: Optional[Dict[str, Any]] = None, search: Optional[str] = None, search_fields: Optional[list] = None):
    """
    Apply dynamic filters and search on a queryset safely.

    :param queryset: Django queryset
    :param filters: dict, e.g., {"is_active": True, "city_id": 1}
    :param search: str, search query
    :param search_fields: list of fields to search in, e.g., ["username", "first_name", "last_name"]
    :return: filtered queryset
    """

    if filters and isinstance(filters, dict) and filters:
        queryset = queryset.filter(**filters)

    if search and search.strip() and search_fields:
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": search})
        queryset = queryset.filter(q_objects)
    return queryset
