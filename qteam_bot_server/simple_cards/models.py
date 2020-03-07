from django.db import models

# Create your models here.
from django.db import models
import json

class CardCategory(models.Model):
    title = models.CharField(max_length=200)
    def num_likes(self, obj):
        likes = CardLike.objects.filter(card=self)
        return len(set([like.bot_user for like in likes]))

    def __str__(self):
        return self.title


class Card(models.Model):
    title = models.CharField(max_length=200)
    card_text = models.CharField(max_length=2000)
    card_cat = models.ForeignKey(CardCategory, on_delete=models.CASCADE)

    is_always = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CardDate(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.card.title + " " + str(self.date)

class BotUser(models.Model):
    bot_user_id    = models.CharField(max_length=30)
    main_resp_path = models.CharField(max_length=30)

    def __str__(self):
        return self.id + ' '+  self.bot_user_id


class BotUserToCardCategory(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card_category = models.ForeignKey(CardCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.bot_user + self.card_category


class CardLike(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.card.title


class CardDislike(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.card.title

class BookEveningEvent(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    planed_date = models.DateField()

    def __str__(self):
        return self.card


class DateUserCardSet(models.Model):
    bot_user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    card_ids = models.CharField(max_length=300, default=json.dumps([]))
    date = models.DateField()

    def __str__(self):
        return self.bot_user + ' ' + self.card_ids