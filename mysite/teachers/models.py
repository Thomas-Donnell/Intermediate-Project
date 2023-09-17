import uuid
from django.contrib.auth.models import User
from django.db import models

class MyClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_descriptor = models.CharField(max_length=50)
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name