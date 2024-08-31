from django.contrib import admin
from django.db.models import Q
from django.utils.html import format_html
from .models import *

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'app', 'user', 'points', 'completed', 'screenshot_preview',)
    search_fields = ('app__name', 'app__category__name', 'app__subcategory__name', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('app', 'completed', 'app__category')
    ordering = ('app', 'user')
    readonly_fields = ('screenshot_preview',)

    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html('<img src="{}" style="width: 100px; height: 100px;"/>', obj.screenshot.url)
        return 'No image'
    screenshot_preview.short_description = 'Screenshot Preview'

    def get_search_results(self, request, queryset, search_term):
        search_term = search_term.strip()
        if not search_term:
            return queryset, False

        queryset = queryset.filter(
            Q(app__name__icontains=search_term) |
            Q(app__category__name__icontains=search_term) |
            Q(app__subcategory__name__icontains=search_term) |
            Q(user__email__icontains=search_term) |
            Q(user__first_name__icontains=search_term) |
            Q(user__last_name__icontains=search_term)
        )

        matching_users = User.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term)
        )

        if matching_users.exists():
            queryset = queryset.filter(user__in=matching_users)
        
        return queryset, False


admin.site.register(Task, TaskAdmin)
admin.site.register(User)