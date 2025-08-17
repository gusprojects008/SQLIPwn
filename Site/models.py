from django.conf import settings
from django.db import models

# Create your models here.

if settings.VULNERABLE == False:
   class UsersCommentsCounts(models.Model):
         username = models.CharField(max_length=100, unique=True)
         comment = models.TextField(unique=True)
         count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], unique=True)
         def __str__(self):
             return self.count
