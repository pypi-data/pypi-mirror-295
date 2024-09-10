from django.contrib import admin
from .models import Tag
from accrete.models import TenantManager


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name', 'color', 'tag_group', 'tenant')
    search_fields = ('name', 'tag_group', 'tenant__name')


admin.site.register(Tag, TagAdmin)
