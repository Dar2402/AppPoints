from django.contrib import admin
from .models import Category, Subcategory, App
from django.utils.html import format_html
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'num_subcategories', 'num_apps')
    search_fields = ('name',)
    ordering = ('name',)

    def num_subcategories(self, obj):
        return obj.subcategories.count()
    num_subcategories.short_description = 'Number of Subcategories'

    def num_apps(self, obj):
        return obj.apps.count()
    num_apps.short_description = 'Number of Apps'

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    ordering = ('category', 'name')

class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description_summary', 'points', 'category', 'subcategory')
    search_fields = ('name', 'description', 'category__name', 'subcategory__name')
    list_filter = ('category', 'subcategory')
    ordering = ('category', 'subcategory', 'name')
    readonly_fields = ('description_summary',)

    def description_summary(self, obj):
        return format_html('<span title="{}">{}</span>', obj.description, obj.description[:50])
    description_summary.short_description = 'Description Summary'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(App, AppAdmin)

