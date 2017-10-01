from django.db import models

class Category(models.Model):
  name = models.TextField()
  level = models.IntegerField()
  parent = models.ForeignKey("self", blank=True, null=True)

