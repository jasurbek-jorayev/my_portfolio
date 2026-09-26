from django.contrib import admin

from .models import Profile, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role_title", "email", "telegram_username")

    def has_add_permission(self, request):
        # Keep this a singleton — edit the existing row instead of adding more.
        return not Profile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_filter = ("category",)
    list_editable = ("order",)
    ordering = ("category", "order", "name")
