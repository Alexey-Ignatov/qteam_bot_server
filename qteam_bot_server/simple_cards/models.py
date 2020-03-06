from django.db import models

# Create your models here.
from django.db import models
import json

class CardCategory(models.Model):
    title = models.CharField(max_length=200)

class Card(models.Model):
    title = models.CharField(max_length=200)
    card_text = models.CharField(max_length=2000)
    card_cat = models.ForeignKey(CardCategory, on_delete=models.CASCADE)

    is_always = models.BooleanField(default=True)


class CardDate(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()

class BotUser(models.Model):
    bot_user_id    = models.CharField(max_length=30)
    main_resp_path = models.CharField(max_length=30)


class BotUserToCardCategory(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card_category = models.ForeignKey(CardCategory, on_delete=models.CASCADE)


class CardLike(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()


class CardDislike(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()

class BookEveningEvent(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    planed_date = models.DateField()


class DateUserCardSet(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card_ids = models.CharField(max_length=300, default=json.dumps([]))
    date = models.DateField()