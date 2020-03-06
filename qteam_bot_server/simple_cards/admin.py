from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Card, CardCategory, CardDate,BookEveningEvent

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(CardCategory)
class CardCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(CardDate)
class CardDateAdmin(admin.ModelAdmin):
    pass


@admin.register(BookEveningEvent)
class BookEveningEventAdmin(admin.ModelAdmin):
    pass

