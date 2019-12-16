from django.contrib import admin

from .models import Template


class TemplateAdmin(admin.ModelAdmin):

    model = Template
    list_display = ['filename', 'vote', 'img_user', 'created_at']
    list_filter = ['img_user', 'vote', 'created_at']
    search_fields = ['filename']


admin.site.register(Template, TemplateAdmin)