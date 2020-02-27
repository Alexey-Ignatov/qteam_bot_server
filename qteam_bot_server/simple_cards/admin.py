from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Card, CardCategory

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    pass


@admin.register(CardCategory)
class CardCategoryAdmin(admin.ModelAdmin):
    pass