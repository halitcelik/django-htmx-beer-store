from django.contrib import admin
from .models import Beer, Style, Category

# Register your models here.


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ("name", "brewery", "category")
    list_filter = ("category", "style")
    list_per_page = 20


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Category)
class StyleAdmin(admin.ModelAdmin):
    list_display = ("name",)
