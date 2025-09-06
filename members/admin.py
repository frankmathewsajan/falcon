from django.contrib import admin
from .models import Member, Task

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "reg_number", "email", "total_credits", "total_tasks", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "reg_number", "email")
    readonly_fields = ("created_at", "updated_at")
    
    def total_credits(self, obj):
        return obj.total_credits()
    total_credits.short_description = "Total Credits"
    
    def total_tasks(self, obj):
        return obj.total_tasks()
    total_tasks.short_description = "Total Tasks"

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "member", "credits", "is_completed", "due_date", "created_at")
    list_filter = ("is_completed", "created_at", "due_date")
    search_fields = ("title", "member__name", "member__reg_number")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("is_completed",)
    
    fieldsets = (
        (None, {
            'fields': ('member', 'title', 'description', 'credits', 'is_completed', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
