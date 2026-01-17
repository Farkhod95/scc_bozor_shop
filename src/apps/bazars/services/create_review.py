from typing import Dict, Any
from django.db import transaction
from django.db.models import Avg, Count
from rest_framework.exceptions import ValidationError

from apps.bazars.models import Bazar, BazarReview



@transaction.atomic
def create_review(*, bazar_id: int, rating: int, user, comment: str = None) -> Dict[str, Any]:
    try:
        bazar = Bazar.objects.get(id=bazar_id)
    except Bazar.DoesNotExist:
        raise ValidationError({"message_key": "bazar_not_found"})

    if BazarReview.objects.filter(bazar=bazar, user=user).exists():
        raise ValidationError({"message_key": "review_already_exists"})

    review = BazarReview.objects.create(
        bazar=bazar,
        user=user,
        rating=rating,
        comment=comment
    )

    return {
        "id": review.id,
        "bazar_id": bazar.id,
        "bazar_name": bazar.name,
        "user": user.id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at
    }
