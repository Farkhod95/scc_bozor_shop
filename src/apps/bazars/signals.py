from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.bazars.models.bazar_review import BazarReview


@receiver(post_save, sender=BazarReview)
@receiver(post_delete, sender=BazarReview)
def update_bazar_rating(sender, instance, **kwargs):
    if instance.bazar:
        instance.bazar.recalculate_rating()