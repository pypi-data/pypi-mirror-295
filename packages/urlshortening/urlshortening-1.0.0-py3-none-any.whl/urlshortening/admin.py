from django.contrib import admin

from urlshortening.models import Url


@admin.register(Url)
class UrlsAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'url', 'pub_date', 'redirect_count')
    ordering = ('-pub_date',)

