from django.db import models

from apps.core.models import BaseModel

class BazarAdmin(BaseModel):
    bazar = models.ForeignKey('Bazar', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username