from django.contrib import admin
from .models import Music


# Register your models here.


class MusicAdmin(admin.ModelAdmin):
    # the list_display admin option, which is a tuple of field names to display,
    # as columns, on the change list page for the object:
    list_display = ('name', 'singer')
    # list_filter = ['name']  过滤器
    search_fields = ['name', 'singer', 'came_from']  # 搜索器,按歌名或者歌手或者来源


admin.site.register(Music, MusicAdmin)
