from django.db import models
import uuid
# Create your models here.
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False)
    createdBy = models.UUIDField(null=False, blank=False)
    createdOn = models.DateTimeField(auto_now_add=True, blank=False)
    description = models.CharField(blank=False, null=False, max_length=500)
    response = models.TextField(blank=False, null=False)
