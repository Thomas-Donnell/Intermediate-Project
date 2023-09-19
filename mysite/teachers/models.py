import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class MyClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_descriptor = models.CharField(max_length=50)
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name
    
    
class EnrolledUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(MyClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    
class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(MyClass, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject