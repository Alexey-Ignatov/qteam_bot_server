from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Card, CardLike, CardDislike,BotUser,BotUserToCardCategory, CardCategory,BookEveningEvent,CardDate,DateUserCardSet
import json
from .views import get_cards_ok_to_show

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display= ('title', 'num_likes', 'num_dislikes',  'num_shows', 'is_available_now','is_active')


    def num_likes(self, obj):
        likes = CardLike.objects.filter(card=obj)
        return len(set([like.bot_user for like in likes]))

    def num_dislikes(self, obj):
        likes = CardDislike.objects.filter(card=obj)
        return len(set([like.bot_user for like in likes]))

    def num_shows(self, obj):
        sets = DateUserCardSet.objects.all()
        return len([True for el in sets if obj.id in json.loads(el.card_ids)])

    def is_available_now(self, obj):
        good_cards = get_cards_ok_to_show()
        return obj in good_cards

    is_available_now.boolean = True
    #fields = ('title', 'num_likes')






@admin.register(CardCategory)
class CardCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(CardDate)
class CardDateAdmin(admin.ModelAdmin):
    pass


@admin.register(BookEveningEvent)
class BookEveningEventAdmin(admin.ModelAdmin):
    pass

@admin.register(CardLike)
class CardLikeAdmin(admin.ModelAdmin):
    pass

@admin.register(CardDislike)
class CardDislikeAdmin(admin.ModelAdmin):
    pass

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    pass


@admin.register(BotUserToCardCategory)
class BotUserToCardCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(DateUserCardSet)
class DateUserCardSetAdmin(admin.ModelAdmin):
    pass







