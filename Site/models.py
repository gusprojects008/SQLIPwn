# Good pratice
'''
from django.db import models

# Create your models here.

class Comment(models.Model):
      base_username = models.CharField(max_length=100)
      user_count = models.CharField(max_length=150, unique=True)
      user_comment = models.TextField()

      def __str__(self):
          return self.username_count
'''
