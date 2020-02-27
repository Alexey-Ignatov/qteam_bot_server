from django.db import models

# Create your models here.
from django.db import models


class CardCategory(models.Model):
    title = models.CharField(max_length=200)

class Card(models.Model):
    title = models.CharField(max_length=200)
    card_text = models.CharField(max_length=2000)

    card_cat = models.ForeignKey(CardCategory, on_delete=models.CASCADE)




class BotUser(models.Model):
    bot_user_id = models.CharField(max_length=30)
    is_romantic = models.BooleanField(default=False)
    is_kulinar = models.BooleanField(default=False)
    is_sport = models.BooleanField(default=False)
    is_partymaker = models.BooleanField(default=False)
    is_edu = models.BooleanField(default=False)
    is_instagram_lover = models.BooleanField(default=False)



class CardLike(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()


class CardDislike(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()
