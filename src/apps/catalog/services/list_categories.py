from typing import Iterable, Dict, Any

from apps.catalog.models import Category


def list_categories() -> Iterable[Dict[str, Any]]:
    categories = Category.objects.all().order_by("-id").values("id", "title", "description", "created_at")
    result = []
    for category in categories:
        result.append({
            "id": category["id"],
            "title": category["title"],
            "description": category["description"],
            "created_at": category["created_at"],
        })
    return result
