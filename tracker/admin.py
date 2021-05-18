from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'status',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'description',
                    'time_entries',
                    'status',
                    'owner',
                )
            },
        ),
    )


admin.site.register(Task, TaskAdmin)
