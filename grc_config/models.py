from django.db import models

from account.models import Account, Audit

class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StatusDB(BaseModel):
    name = models.CharField(max_length=32)