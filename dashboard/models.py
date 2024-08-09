from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Backup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=13, unique=True)
    date = models.DateField(unique=False, null=True)
    time = models.CharField(max_length=60,null=False,unique=True )
    def __str__(self):

        return f'{self.user.email} Backed up Database'