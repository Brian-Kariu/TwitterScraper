from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from app.models import TweetData

# Register your models here.


@admin.register(TweetData)
class TweetDataAdmin(SimpleHistoryAdmin):
    list_display = ("text",)
    history_list_display = ("text",)
    search_fields = ("text",)
    list_filter = ("text",)
