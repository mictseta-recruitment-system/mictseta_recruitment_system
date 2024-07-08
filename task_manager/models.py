from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} category"

class Task(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=20,default="low", null=False)
    description = models.TextField(max_length=225 , null=False)
    date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"Task {self.name} from category {self.category.name}"