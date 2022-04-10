from csv import list_dialects
from django.contrib import admin
from .models import *


class CardAdmin(admin.ModelAdmin):
    model = Card
    list_display = ('id', 'title', 'order')


admin.site.register(Card, CardAdmin)
