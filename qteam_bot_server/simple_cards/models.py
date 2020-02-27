from django.db import models

# Create your models here.
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200)

class Card(models.Model):
    title = models.CharField(max_length=200)
    card_text = models.CharField(max_length=2000)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)







